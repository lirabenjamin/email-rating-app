library(arrow)
library(dotenv)
library(mongolite)
load_dot_env()

# set up connection
mongo_uri <- Sys.getenv("MONGO_URI")
mongo_conn <- mongo(db = "ratings", collection = "responses", url = mongo_uri)

# load data
ai_rewrites <- mongo_conn$find() %>% as_tibble() %>% 
  mutate_at(vars(q1:q5), as.numeric) %>%
  mutate(average = (q1 + q2 + q3 + q4 + q5) / 5) 
ai_rewrites %>% count(ra_name)

clean = read_parquet("clean.parquet") %>% 
  select(id, matches("test_rewritten")) %>% 
  select(email_id = id, q1 = less_is_more_test_rewritten, q2 = easy_reading_test_rewritten, q3 = easy_navigation_test_rewritten, q4 = formatting_test_rewritten, q5 = easy_responding_test_rewritten, average = average_test_rewritten)  %>% 
  mutate(ra_name = "gpt")

merge = ai_rewrites %>% 
  filter(ra_name %in% c("Ben","Maya")) %>% 
  group_by(email_id) %>%
  summarise(across(q1:average, \(x) mean(x, na.rm = TRUE)))  %>% 
  mutate(ra_name = "merge")

ids = (merge$email_id)
ai_rewrites = ai_rewrites %>% 
  bind_rows(clean %>% filter(email_id %in% ids)) %>% 
  bind_rows(merge) 

batch1_start = as_datetime("2024-10-24 14:36:10 EDT")
batch1_end = as_datetime("2024-10-24 15:02:01 EDT")

colnames(clean)

ai_rewrites %>% 
  select(-timestamp)  %>% 
  pivot_longer(cols = c(q1:q5,average), names_to = "question", values_to = "rating")  %>% 
  pivot_wider(names_from = ra_name, values_from = rating)  %>%
  mutate(
    question = case_match(
      question,
      "q1" ~ "Less is More",
      "q2" ~ "Easy Reading",
      "q3" ~ "Easy Navigation",
      "q4" ~ "Formatting",
      "q5" ~ "Easy Responding",
      "average" ~ "Average"

    )
  ) %>%
  mutate(question = fct_inorder(question))  %>%
  ggplot(aes(x = Maya, Ben))+ 
  geom_jitter(size = 3, alpha = .3) +
  scale_x_continuous(limits = c(0, 10), breaks = 0:10) +
  scale_y_continuous(limits = c(0, 10), breaks = 0:10) +
  # coord_fixed() +
  ggpubr::stat_cor(method = "pearson") +
  geom_smooth(method = "lm") +
  geom_abline(intercept = 0, slope = 1, color = 'red') +
  facet_wrap(~question, scales = "fixed") +
  labs(x = "Maya", y = "Ben")
ggsave("ratings.png", width = 6, height = 4)


ai_rewrites  %>% 
  select(ra_name, email_id, q5) %>% 
  pivot_wider(names_from = ra_name, values_from = q5) 

ai_rewrites %>% 
  select(-timestamp)  %>% 
  pivot_longer(cols = c(q1:q5,average), names_to = "question", values_to = "rating")  %>% 
  pivot_wider(names_from = ra_name, values_from = rating)  %>%
  mutate(
    question = case_match(
      question,
      "q1" ~ "Less is More",
      "q2" ~ "Easy Reading",
      "q3" ~ "Easy Navigation",
      "q4" ~ "Formatting",
      "q5" ~ "Easy Responding",
      "average" ~ "Average"

    )
  ) %>%
  mutate(question = fct_inorder(question))  %>%
  ggplot(aes(x = gpt, merge))+ 
  geom_jitter(size = 3, alpha = .3) +
  scale_x_continuous(limits = c(0, 10), breaks = 0:10) +
  scale_y_continuous(limits = c(0, 10), breaks = 0:10) +
  # coord_fixed() +
  ggpubr::stat_cor(method = "pearson") +
  geom_smooth(method = "lm") +
  geom_abline(intercept = 0, slope = 1, color = 'red') +
  facet_wrap(~question, scales = "fixed") +
  labs(x = "GPT", y = "Ben Maya Average")
ggsave("ratings_gpt.png", width = 6, height = 4)

library(dotenv)
library(mongolite)

load_dot_env()


mongo_uri <- Sys.getenv("MONGO_URI")
mongo_conn <- mongo(db = "ratings", collection = "responses", url = mongo_uri)

ai_rewrites <- mongo_conn$find() %>% as_tibble()
ai_rewrites %>% count(ra_name)


ai_rewrites %>% 
  select(-timestamp) %>%
  mutate_at(vars(q1:q5), as.numeric) %>%
  mutate(average = (q1 + q2 + q3 + q4 + q5) / 5)  %>% 
  pivot_longer(cols = c(q1:q5,average), names_to = "question", values_to = "rating")  %>% 
  pivot_wider(names_from = ra_name, values_from = rating)  %>%
  ggplot(aes(x = Maya, Ben))+ 
  geom_point() +
  ggpubr::stat_cor(method = "pearson") +
  geom_smooth(method = "lm") +
  geom_abline(intercept = 0, slope = 1, color = 'red') +
  facet_wrap(~question, scales = "free") +
  labs(title = "Maya vs Ben", x = "Maya", y = "Ben")



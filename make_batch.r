library(arrow)
library(gt)
size = 20

data = read_parquet("clean.parquet")

data %>% arrange(average_test_rewritten) %>% 
  select(id, test_rewritten, matches('_test_rewritten')) %>% slice(1, 1001, 2002) %>% select(test_rewritten) %>%
    gt::gt() %>% 
    fmt_markdown() 

set.seed(14235)
data %>% slice_sample(n = size) %>% select(id, test_rewritten) %>% write_parquet("instance/batch2.parquet")

data %>% select(matches("_test_re")) %>% 
  summarise_all(max)

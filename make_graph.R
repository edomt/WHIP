library(ggplot2)
library(scales)
library(dplyr)

df <- readr::read_csv('prepared.csv') %>%
  arrange(group)

g <- ggplot(data = df, aes(x = date, y = dissent, color = group)) +
  geom_smooth(method = "loess", se = FALSE, size = 1.5) +
  labs(title = "Évolution de l'opposition interne",
     y = "Tendance d'opposition interne (% des membres)",
     x = NULL) +
  scale_y_continuous(labels = scales::percent_format(accuracy = 1)) +
  scale_color_manual(values = c("#FF0000", "#FF8000", "#990000", "#FFEB00", "#0066CC", "#999999", "#FF8080", "#30BFE9")) +
  theme_grey(base_size = 10.5) +
  theme(legend.title = element_blank(), legend.position = "bottom")

ggsave(g, filename = "whip_graph.png", width = 10, height = 5, units = "in")

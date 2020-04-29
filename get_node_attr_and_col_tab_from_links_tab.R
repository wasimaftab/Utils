cat('\014')
rm(list = ls())

links <- readxl::read_xlsx('Bait_Prey_FClog.xlsx')

## create node attr. table
name <- union(links$source, links$target)
group <- rep('Preys', length(name))
bait_proteins <- c('Setdb1', 'Atf7ip', 'Morc3')
bait <- rep(FALSE, length(name))
idx_bait <- which(name %in% bait_proteins)
bait[idx_bait] <- TRUE
border_color <- rep('#999', length(name))
border_color[idx_bait] <- '#000'
group[idx_bait] <- bait_proteins
# border_color[idx_bait] <- '#0FF'
node_attr_pool <- as.data.frame(cbind(name, group, bait, border_color))
colnames(node_attr_pool)[ncol(node_attr_pool)] <- 'borderColor'
# writexl::write_xlsx(node_attr_pool, 'node_attr_tab.xlsx')

## create color table
group <-sort(unique(group))
if (length(group) > 4) {
    stop(paste('there are more than', length(group), 'groups, so adapt your code'))
}else{
    color <- c('#F3C', '#FF3', '#666', '#30F')
    # color <- c('#F3C', '#FF3', '#3CF', '#0C3', '#C6F', '#30F', '#666')
}
group_color <- as.data.frame(cbind(group, color))
browser()

writexl::write_xlsx(group_color, 'group_color.xlsx')

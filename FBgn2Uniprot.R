cat("\014")
rm(list = setdiff(ls(), "db"))

## load the db CONTAINING MAPPING
# db <- as.data.frame(read.delim2("~/Desktop/New SWATH/fbgn_NAseq_Uniprot_fb_2020_02.tsv",
#                                sep = "\t",
#                                stringsAsFactors = FALSE))
idx_dmel <- which(db$organism_abbreviation == "Dmel")

db2 <- db[idx_dmel,]
idx_blank <- which(db2$UniprotKB.Swiss.Prot.TrEMBL_accession == "")
db2 <- db2[-idx_blank,]
A <- db2$primary_FBgn
idx_unique_FBgn <- order(A)[!duplicated(sort(A))]
db2 <- db2[idx_unique_FBgn,]
db2 <- db2[,c(1:3, ncol(db2)-3)]

## sort db2 based on symbols
x <- sort(db2$gene_symbol, index.return=TRUE)
db2 <- db2[x$ix,]

## load the gold standard FBgns
# FBgn_SEC_42 <- read.table("~/Desktop/New SWATH/Fbgn_SEC_Axel_42_Fr", 
#                           sep = "\n", 
#                           col.names = c("FBgn"), 
#                           stringsAsFactors = FALSE)
# 
# idx_FBgn <- which(db2$primary_FBgn %in% FBgn_SEC_42$FBgn)
# FBgn_mapped <- unique(db2$primary_FBgn[idx_FBgn])
# Uniprot_mapped <- 
# FBgn_not_mapped <- setdiff(FBgn_SEC_42$FBgn, FBgn_mapped)

## load SEC data 42 fractions
SEC1 <- as.data.frame(readxl::read_xlsx("~/Desktop/New SWATH/SEC_molwt_complex_annotated_compressed_using_STRING_Andreas_Gold_std.xlsx",
                                        sheet = 1))
idx_FBgn_in_db <- which(db2$primary_FBgn %in% SEC1$Gene)
FBgn_mapped <- unique(db2$primary_FBgn[idx_FBgn_in_db])
FBgn_not_mapped <- setdiff(SEC1$Gene, FBgn_mapped)
idx_not_mapped_in_SEC <- which(SEC1$Gene %in% FBgn_not_mapped)
SEC1 <- SEC1[-idx_not_mapped_in_SEC,] 
idx_FBgn_in_db <- which(db2$primary_FBgn %in% SEC1$Gene)
uniprot_mapped <- db2$UniprotKB.Swiss.Prot.TrEMBL_accession[idx_FBgn_in_db]
SEC_test <- cbind(uniprot_mapped, SEC1[,7:ncol(SEC1)])

# symbols_not_mapped <- SEC1$Symbol[idx_not_mapped]
# SEC2 <- as.data.frame(readxl::read_xlsx("~/Desktop/New SWATH/SEC_molwt_complex_annotated_compressed_using_STRING_Andreas_Gold_std.xlsx",
#                          sheet = 2))
# SEC2 <- SEC2[-idx_not_mapped,]
# ## sort SEC2 based on symbols
# x <- sort(SEC2$Symbol, index.return=TRUE)
# SEC2 <- SEC2[x$ix,]
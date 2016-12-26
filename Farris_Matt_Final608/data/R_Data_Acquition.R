#Taking Data Directly from Github page for simplicity.
library(RCurl)
library(plyr)
url <- "https://raw.githubusercontent.com/mfarris9505/Medicare/master/data/IPPS_All_DRG.csv"
dat <- getURL(url, ssl.verifypeer=0L, followlocation=1L)
dat <- read.csv(text=dat)

all_drg <-data.frame(dat)
all_drg$DRG.Code <- lapply(strsplit(as.character(all_drg$DRG.Definition), "\\ -"), "[", 1)

#Necessary DRG Codes 
COPD_DRG <- c("190","191","192")
PN_DRG <- c("193","194","195")
HF_DRG <- c("291","292","293")
AMI_DRG <- c("280","281","282","283","284","285")

#Location Info
url <- "https://raw.githubusercontent.com/mfarris9505/Medicare/master/data/Hosp_Info.csv"
dat <- getURL(url, ssl.verifypeer=0L, followlocation=1L)
dat <- read.csv(text=dat)

hosp_info <-data.frame(dat)
hosp_info$Lat <- lapply(strsplit(as.character(hosp_info$Location), "\\("), "[", 2)
hosp_info$Long <- lapply(strsplit(as.character(hosp_info$Lat), "\\,"), "[", 2)
hosp_info$Lat <- lapply(strsplit(as.character(hosp_info$Lat), "\\,"), "[", 1)
hosp_info$Long <- lapply(strsplit(as.character(hosp_info$Long), "\\)"), "[", 1)
hosp_info$Long <- as.numeric(hosp_info$Long)
hosp_info$Lat <- as.numeric(hosp_info$Lat)
col_keep <- c("X.U.FEFF.Provider.ID", "Lat", "Long")
hosp_info <- hosp_info[,col_keep]
colnames(hosp_info) <- c("Provider.Id","Lat","Long")


#Readmission and Mortality Data 
url <- "https://raw.githubusercontent.com/mfarris9505/Medicare/master/data/Readm_Mort_Hosp.csv"
dat <- getURL(url, ssl.verifypeer=0L, followlocation=1L)
dat <- read.csv(text=dat)

mort_readm <-data.frame(dat)

row_remove <- c("READM_30_HOSP_WIDE", "READM_30_HIP_KNEE","MORT_30_CABG",
                "READM_30_CABG","MORT_30_STK","READM_30_STK")
mort_readm <- mort_readm[!mort_readm$Measure.ID %in% row_remove,]
col_keep <- c("Provider.ID", "Measure.ID","Score")
mort_readm_val <- mort_readm[,col_keep]
mort_readm_val <- reshape(mort_readm_val, idvar = "Provider.ID", 
                             timevar = "Measure.ID", direction = "wide")
colnames(mort_readm_val) <- c("Provider.Id","MORT.AMI","MORT.COPD","MORT.HF",
                                 "MORT.PN","READM.AMI","READM.COPD","READM.HF",
                                 "READM.PN")

#Prices Split By DRG
hf_drg <- all_drg[all_drg$DRG.Code %in% HF_DRG,]
hf_drg$Comb.DRG <- "HF"
pn_drg <- all_drg[all_drg$DRG.Code %in% PN_DRG,]
pn_drg$Comb.DRG <- "PN"
copd_drg <- all_drg[all_drg$DRG.Code %in% COPD_DRG,]
copd_drg$Comb.DRG <- "COPD"
ami_drg <- all_drg[all_drg$DRG.Code %in% AMI_DRG,]
ami_drg$Comb.DRG <- "AMI"

hf_mort <- mort_readm_val[,c("Provider.Id","MORT.HF","READM.HF")]
colnames(hf_mort) <- c("Provider.Id","MORT","READM")
pn_mort <- mort_readm_val[,c("Provider.Id","MORT.PN","READM.PN")]
colnames(pn_mort) <- c("Provider.Id","MORT","READM")
copd_mort <- mort_readm_val[,c("Provider.Id","MORT.COPD","READM.COPD")]
colnames(copd_mort) <- c("Provider.Id","MORT","READM")
ami_mort <- mort_readm_val[,c("Provider.Id","MORT.AMI","READM.AMI")]
colnames(ami_mort) <- c("Provider.Id","MORT","READM")

#Combine Prices and Scores 
hf_drg <- join(hf_drg, hf_mort, by="Provider.Id", type="left")
pn_drg <- join(pn_drg, pn_mort, by="Provider.Id", type="left") 
copd_drg <- join(copd_drg, copd_mort, by="Provider.Id", type="left")
ami_drg <- join(ami_drg, ami_mort, by="Provider.Id", type="left")
get
#Combine to One File
tol_data <- do.call("rbind",list(hf_drg,pn_drg,copd_drg,ami_drg))
tol_data <- join(tol_data, hosp_info, by="Provider.Id", type="left")

#Zip-County Crosswalk Folder


url <- "https://raw.githubusercontent.com/mfarris9505/Medicare/master/data/ZIP_FIPS.csv"
dat <- getURL(url, ssl.verifypeer=0L, followlocation=1L)
dat <- read.csv(text=dat, stringsAsFactors = TRUE)
zip_count <- data.frame(dat)
names(tol_data)[names(tol_data) == "Provider.Zip.Code"] <- "ZIP"
tol_data <- join(tol_data, zip_count, by="ZIP", type="left")



tol_data <- data.frame(lapply(tol_data, as.character), stringsAsFactors=FALSE)
setwd("C:/Users/Matthew/Documents")
write.table(tol_data, file = "Total_Data.csv", sep = ",")


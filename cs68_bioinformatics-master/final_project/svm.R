#load the svm library
library(e1071)

#load the data
proteins <- read.csv("/home/eoh1/cs68/cs68_bioinformatics/5/input/leukemiaPatients.csv", header=TRUE)

#get number of columns and rows
col <- ncol(proteins)
row <- nrow(proteins)

#get id and class columns
#id <- proteins[,1]
class <- as.character(proteins[,col])

#remove id and class columns so only left with attributes
attributes <- proteins[,c(-col)]

#designate what percent of data to use as training 
ntrain <- round(row*0.75)

#create train and test sets
trainindex <- sample(row,ntrain) #indices of training samples
train <- attributes[trainindex,]
test <- attributes[-trainindex,]
classtrain <- class[trainindex]
classtest <- class[-trainindex]

#run the no CV model
svmmodel <- svm(train, classtrain, type = "C-classification", kernel="linear")

#run the CV model
#svmmodel <- svm(attributes, class, type = "C-classification", kernel="linear", cross=20)

#make predictions
predictions <- predict(svmmodel,test)

#confusion matrix
tab <- table(pred = predictions, true = classtest)

#write matrix to file
write.table(tab,"confusion.txt")
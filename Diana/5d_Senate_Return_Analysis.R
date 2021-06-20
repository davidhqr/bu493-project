#Preliminary Analysis on 1d Abnormal Returns

Data=read.csv("C:/Users/ASUS/Desktop/5d_senate_returns.csv",header=T)
attach(Data)
Model1 <- lm(return_abnormal_5d ~ as.factor(owner)+as.factor(type)+as.factor(Senator)+Age+In_Office+as.factor(Party)
             +Data$Budget
             +Data$Environment_and_Public_Works
             +Data$Homeland_Security_and_Governmental_Affairs
             +Data$Judiciary
             +Data$Rules_and_Administration
             +Data$Agriculture_Nutrition_and_Forestry
             +Data$Commerce_Science_and_Transportation
             +Data$Armed_Services
             +Data$Energy_and_Natural_Resources
             +Data$Finance
             +Data$Foreign_Relations
             +Data$Small_Business_and_Entrepreneurship
             +Data$Health_Education_Labor_and_Pensions
             +Data$Banking_Housing_and_Urban_Affairs
             +Data$Veterans_Affairs
             +Data$Appropriations, 
             data=Data)
summary(Model1)


faraway::vif(proteinModel)
threshold=10
drop=TRUE
aftervif=data.frame()
while(drop==TRUE) {
  vModel1=faraway::vif(Model1)
  aftervif=rbind.fill(aftervif,as.data.frame(t(vModel1)))
  if(max(vModel1)>threshold) { 
    Model1 = update(Model1,as.formula(paste(".","~",".","-",names(which.max(vModel1))))) 
  }
  else { 
    drop=FALSE 
  }
}

bc <- boxcox(Model1)
lambda <- bc$x[which.max(bc$y)]
Model1_2 <- Model1
update(Model1_2, (return_abnormal_1d^lambda-1)/lambda ~ .)

plot(Model1_2$fitted.values, Model1_2$residuals, xlab = "Fitted Values", ylab = "Residuals")
plot(Model1_2$residuals, xlab = "Index", ylab = "Residuals")
qqnorm(Model1_2$residuals)
qqline(Model1_2$residuals, col="blue", lwd = 2)

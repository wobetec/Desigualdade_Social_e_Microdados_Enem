library(tidyverse)
library(ggplot2)
library(dplyr)
library(readr)
library(lme4)
library(caret)
library(Matrix)
library(MuMIn)
library(performance)
library(arrow)

df <- read_feather("../data/filtered_cat.feather")

full_model <- lm(NU_NOTA ~ Q001 + Q002 + Q003 + Q004 + Q005 + Q006 + Q007 + Q008 + Q009 + Q010 + Q011 + Q012 + Q013 + Q014 + Q015 + Q016 + Q017 + Q018 + Q019 + Q020 + Q021 + Q022 + Q023 + Q024 + Q025, data=df)

summary(full_model)

# remove Q009 e Q023
full_model <- lm(NU_NOTA ~ Q001 + Q002 + Q003 + Q004 + Q005 + Q006 + Q007 + Q008 + Q010 + Q011 + Q012 + Q013 + Q014 + Q015 + Q016 + Q017 + Q018 + Q019 + Q020 + Q021 + Q022 + Q024 + Q025, data=df)
summary(full_model)

coefficients <- summary(full_model)$coefficients
coefficients_df <- as.data.frame(coefficients)
write.csv(coefficients_df, file = "../data/full_model.csv", row.names = TRUE)

full_model_aic <- AIC(full_model)
full_model_aic

full_model_r2 <- r2(full_model)
full_model_r2

full_model_pred <- predict(full_model) 
full_model_mse <- mean((df$NU_NOTA - full_model_pred)^2)
full_model_mse

# varying-intercept model
intercept_model <- lmer(NU_NOTA ~ Q001 + Q002 + Q003 + Q004 + Q005 + Q006 + Q007 + Q008 + Q010 + Q011 + Q012 + Q013 + Q014 + Q015 + Q016 + Q017 + Q018 + Q019 + Q020 + Q021 + Q022 + Q024 + Q025 + (1 | SG_UF_PROVA), data=df)
summary(intercept_model)

coefficients <- summary(intercept_model)$coefficients
coefficients_df <- as.data.frame(coefficients)
write.csv(coefficients_df, file = "../data/intercept_model.csv", row.names = TRUE)

UF_effect <- ranef(intercept_model)$SG_UF_PROVA
UF_effect

UF_effect_df <- as.data.frame(UF_effect)
write.csv(UF_effect_df, file = "../data/UF_effect.csv", row.names = TRUE)

intercept_model_aic <- AIC(intercept_model)
intercept_model_aic

intercept_model_r2 <- r2(intercept_model)
intercept_model_r2

intercept_model_pred <- predict(intercept_model) 
intercept_model_mse <- mean((df$NU_NOTA - intercept_model_pred)^2)
intercept_model_mse



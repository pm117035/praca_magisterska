#Wyczyszczenie środowiska
rm(list=ls())

#Dołączenie bibliotek
library(ggplot2)
library(dplyr)

#Wczytanie danych do ramki danych 'dane' i ich wyświetlenie
dane <- read.table(file="C:\\Users\\piotr\\Desktop\\Gotowe pliki\\praca_magisterska\\1. Dane.csv", sep=";", dec=".", header=T, stringsAsFactors=F)
View(dane)

#Połączenie 'Dzien' i 'Godzina' w jedną kolumnę 'Data', konwersja 'Data' do postaci daty oraz usunięcie temperatur > 10°C 
dane$Data <- paste(dane$Dzien, dane$Godzina)
dane <- dane[,-2]
dane <- dane[,-2]
dane$Data <- as.POSIXct(dane$Data, format="%d.%m.%Y %H:%M")
dane <- subset(dane, Temperatura < 10)

#Histogram temperatury podczas transportu żywności w kontenerze drogą morską
hist(dane$Temperatura, xlim=c(0,7), breaks=50, col=c("red"), xlab="Temperatura", ylab="Częstotliwość wystąpienia", main="Histogram temperatury podczas transportu żywności w kontenerze drogą morską")
abline(h=5, lty=3, col="black")
abline(h=50, lty=3, col="black")
abline(h=100, lty=3, col="black")
abline(h=300 ,lty=3, col="black")
abline(h=500 ,lty=3, col="black")
abline(h=700 ,lty=3, col="black")

#Podstawowe informacje i statystyki dla temperatury mierzonej podczas badania
nrow(dane)
min(dane$Temperatura)
max(dane$Temperatura)
median(dane$Temperatura)
mean(dane$Temperatura)

#Ponowne wczytanie danych, tym razem do ramki danych 'dane2' i wypisanie podstawowych statystyk
dane2 <- read.table(file="C:\\Users\\piotr\\Desktop\\Gotowe pliki\\praca_magisterska\\1. Dane.csv", sep=";", dec=".", header=T, stringsAsFactors=F)
nrow(dane2)
min(dane2$Temperatura)
max(dane2$Temperatura)
median(dane2$Temperatura)
mean(dane2$Temperatura)

#Wykres pudełkowy, określający rozkład mierzonych temperatur podczas transportu
summary(dane$Temperatura)
boxplot(dane$Temperatura, col=("yellow"), main="Rozkład mierzonych temperatur podczas transportu")
abline(h=min(dane$Temperatura) ,lty=3, col="black")
abline(h=max(dane$Temperatura) ,lty=3, col="black")
abline(h=median(dane$Temperatura) ,lty=3, col="black")

#Wartości odstające 
Outliers = boxplot(dane$Temperatura, plot=FALSE)$out
show(Outliers)
summary(Outliers)

#Wykres Temperatury od Daty
plot(dane$Data,dane$Temperatura, type="l", col=c("blue"), xlab="Data" , ylab="Temperatura", main="Wartość temperatury podczas transportu")
abline(h=0.5, lty=3, col="black")
abline(h=1, lty=3, col="black")
abline(h=1.5, lty=3, col="black")
abline(h=2, lty=3, col="black")

#Ponowne wczytanie danych, tym razem do ramki danych 'dane3' oraz stworzenie dwóch modeli regresji liniowej
dane3 <- read.table(file="C:\\Users\\piotr\\Desktop\\Gotowe pliki\\praca_magisterska\\1. Dane.csv", sep=";", dec=".", header=T, stringsAsFactors=F)
dane3$Dzien <- as.Date(dane3$Dzien, format="%d.%m.%Y")
dane3$Godzina <- as.POSIXct(dane3$Godzina, format="%H:%M")
dane3 <- subset(dane3, Temperatura < 10)
model1 <- lm(Temperatura ~ Dzien, data = dane3)
summary(model1)
model2 <- lm(Temperatura ~ Godzina, data = dane3)
summary(model2)

#Grupowanie danych po 'Dzien' oraz 'Godzina'
grupa1 <- group_by(dane3, Temperatura, Dzien)
licz1 <- count(select(grupa1))
licz1 <- rename(licz1, Licza_wystąpień1=n)

grupa2 <- group_by(dane3, Temperatura, Godzina)
licz2 <- count(select(grupa2))
licz2 <- rename(licz2, Licza_wystąpień2=n)

#Rozkłady temperatury w zależności od dnia oraz godziny
x11();
ggplot(licz1, aes(Temperatura, Dzien, size=Licza_wystąpień1), colour = I("blue")) + 
  geom_point(aes(alpha = Licza_wystąpień1), colour = I("blue")) +
  xlab ("Temperatura") + 
  ylab ("Dzien")

x11();
ggplot(licz2, aes(Temperatura, Godzina, size=Licza_wystąpień2), colour = I("blue")) + 
  geom_point(aes(alpha = Licza_wystąpień2), colour = I("blue")) +
  xlab ("Temperatura") + 
  ylab ("Godzina")
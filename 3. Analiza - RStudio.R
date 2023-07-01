#Wyczyszczenie środowiska
rm(list=ls())

#Dołączenie bibliotek
library(ggplot2)
library(dplyr)
library(scales)
library(timetk)

#Wczytanie danych do ramki danych 'dane' i ich wyświetlenie
dane <- read.table(file="C:\\Users\\piotr\\Desktop\\Dane.csv", sep=";", dec=".", header=T, stringsAsFactors=F)
View(dane)

#Połączenie 'Dzien' i 'Godzina' w jedną kolumnę 'Data' oraz konwersja do postaci daty 
dane$Data <- paste(dane$Dzien, dane$Godzina)
dane <- dane[,-2]
dane <- dane[,-2]
dane$Data <- as.POSIXct(dane$Data, format="%d.%m.%Y %H:%M")

#Podział danych na okresy, według przypuszczeń, co do aktualnego położenia transportu
dane <- dane %>% 
  mutate(
    Okres = case_when(
      Data %>% between_time ("2022-11-16 00:09:00", "2022-11-18 23:57:00") ~ "1 Belsk Duży - Gdańsk, Polska",
      Data %>% between_time ("2022-11-19 00:09:00", "2022-11-25 23:57:00") ~ "2 Morze Bałtyckie i Morze Północne",
      Data %>% between_time ("2022-11-26 00:09:00", "2022-12-05 23:57:00") ~ "3 Ocean Atlantycki oraz Morze Śródziemne",
      Data %>% between_time ("2022-12-06 00:09:00", "2022-12-24 23:57:00") ~ "4 Kanał Sueski, Morze Czerwone i Morze Arabskie",
      T ~ "5 Navi Mumbai, Indie")
  )

#Wykres temperatury podczas transportu jabłek drogą morską w kontenerze
ggplot(dane, aes(x=Data, y=Temperatura, color=Okres)) +
  geom_line(linewidth=0.8) + 
  xlab("Data") + 
  ylab("Temperatura [°]") + 
  ggtitle("Temperatura podczas transportu jabłek drogą morską w kontenerze") +
  theme(plot.title = element_text(hjust = 0.5)) +
  scale_x_datetime(date_breaks = "1 day", date_labels ="%d.%m.%Y") +
  theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust=1)) +
  scale_y_continuous(limits = c(0,26), breaks=seq(0,26,2)) +
  theme(legend.position = c(0.22, 0.80),
        legend.title = element_text(size=13, face="bold"),
        legend.text = element_text(colour="blue", size=10, face="bold"),
        legend.background = element_rect(linewidth=0.5, linetype="solid", colour ="darkblue"))

#Usunięcie temperatur > 10°C 
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
dane2 <- read.table(file="C:\\Users\\piotr\\Desktop\\Dane.csv", sep=";", dec=".", header=T, stringsAsFactors=F)
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
Outliers = boxplot(dane$Temperatura, plot=F)$out
Outliers_ind <- which(dane$Temperatura %in% c(Outliers))
dane[Outliers_ind, ]
summary(Outliers)

#Wykres wartości temperatury podczas transportu
plot(dane$Data,dane$Temperatura, type="l", col=c("blue"), xlab="Data" , ylab="Temperatura", main="Wartość temperatury podczas transportu")
abline(h=0.5, lty=3, col="black")
abline(h=1.8, lty=3, col="black")
abline(h=4, lty=1, col="black")

#Ponowne wczytanie danych, tym razem do ramki danych 'dane3'
dane3 <- read.table(file="C:\\Users\\piotr\\Desktop\\Dane.csv", sep=";", dec=".", header=T, stringsAsFactors=F)
dane3$Dzien <- as.Date(dane3$Dzien, format="%d.%m.%Y")
dane3$Godzina <- as.POSIXct(dane3$Godzina, format="%H:%M")
dane3 <- subset(dane3, Temperatura < 10)

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
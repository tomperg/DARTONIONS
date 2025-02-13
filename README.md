

# DARTONIONS  
**Dartwurfanalyse-Projekt von Amelie, Eric und Thomas**  

## 🏹 Idee  
Dart ist ein Sport mit vergleichsweise wenigen externen Einflüssen. Unser Ziel ist es, Spielerinnen und Spielern dabei zu helfen, ihren perfekten Wurf zu finden. Dafür analysieren wir zwei entscheidende Parameter:  

- **Geschwindigkeit** des Darts beim Loslassen  
- **Winkel des Unterarms** im Moment des Abwurfs  

Durch diese Daten können individuelle Optimierungen vorgenommen und präzisere Würfe erzielt werden.  

## 🔄 Ablauf des Codes  
1. Das System läuft im **Standby-Modus**, bis die IMU-Messung über das Touchpad aktiviert wird.  
2. Die Messung endet automatisch mit dem **Loslassen des Darts**.  
3. Während des Abwurfs erfasst die IMU **den Winkel des Unterarms** und die **Abwurfgeschwindigkeit**.  
4. Die Ergebnisse werden auf einem **Webserver** visualisiert.  

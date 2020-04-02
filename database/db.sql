-- MySQL dump 10.13  Distrib 5.7.27, for Linux (x86_64)
--
-- Host: cwittmann.mysql.pythonanywhere-services.com    Database: cwittmann$default
-- ------------------------------------------------------
-- Server version	5.6.40-log

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `building`
--

DROP TABLE IF EXISTS `building`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `building` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` text,
  `description` text,
  `lat` decimal(9,6) DEFAULT NULL,
  `lng` decimal(9,6) DEFAULT NULL,
  `parentId` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=98266272 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `building`
--

LOCK TABLES `building` WRITE;
/*!40000 ALTER TABLE `building` DISABLE KEYS */;
INSERT INTO `building` VALUES (7507359,'Pfarrhof St. Sebald','Zur Sebalduskirche gehört der gegenüber liegende Sebalder Pfarrhof. Er ist hauptsächlich um 1361/1379 entstanden. Hier wohnten einst der Sebalder Klerus: Prediger, Diakone, „Schaffer“ (Verwalter) und Bedienstete.',49.455139,11.075917,88575206),(13151930,'Brauttor St. Sebald','Mittig an der Nordfassade liegt das „Brauttor“ genannte überdachte Portal, an dem (vor der Einführung der Brautmesse) die ab dem Tridentinischen Konzil vorgeschriebene kirchliche Trauung stattfand.',49.455139,11.075917,88575206),(15481914,'Alte Hofhaltung','Die Alte Hofhaltung ist ein historischer Gebäudekomplex in Bamberg. Sie besteht aus ehemaligen Wohn- und Wirtschaftsgebäuden der bischöflichen Hofhaltung, die ab dem 15. Jahrhundert an der Stelle der Pfalz Kaiser Heinrichs II. errichtet wurden. ',49.891111,10.881389,0),(17402759,'Nassauer Haus','Das Nassauer Haus oder Schlüsselfeldersche Stiftungshaus in Nürnberg ist ein mittelalterlicher Wohnturm aus sogenanntem roten Burgsandstein. Zwar ursprünglich in romanischem Stil erbaut, kennzeichnen das Haus nach einigen Umbauten bis heute gotische Stilelemente.',49.451111,11.077725,0),(19215168,'Nordwestfassade','Erwähnenswert sind die ursprünglich 1755 von Johann Anwander geschaffenen Fassadenmalereien, die vielfach restauriert wurden. Nachdem von diesen Bemalungen in den 1950er Jahren nicht mehr viel zu sehen war, wurde durch den Kunstmaler Anton Greiner in den Jahren 1959 bis 1962 eine Neubemalung vorgenommen. Beide Gebäudeseiten sind vollständig mit nachempfundenen allegorischen Szenen und architektonischen Details, der typischen Illusionsmalerei in dieser Zeit, verziert. Kleine, tatsächlich figürlich gestaltete Elemente an der östlichen Seite verstärken den räumlichen Eindruck. Die Rokokobalkons und Wappenreliefs stammen von Jos. Bonaventura Mutschele.',49.891667,10.886944,94710860),(19996675,'Neue Residenz','Die Neue Residenz ist ein mehrflügeliges denkmalgeschütztes Gebäude am Domplatz im oberfränkischen Bamberg. Es war ab 1602 die Residenz der Bamberger Fürstbischöfe und löste die Alte Hofhaltung auf der anderen Seite des Platzes in dieser Funktion ab. Heute beherbergt der Komplex aus Sandstein die Staatsbibliothek und die Staatsgalerie von Bamberg.',49.891667,10.882500,0),(23188669,'Brückenturm','n der Fassade des Brückenturmes fallen zunächst die Rokoko-Balkone auf und darüber ein Wappen, das auf einen der letzten Fürstbischöfe von Bamberg hindeutet. Es handelt sich dabei um Franz Konrad Graf von Stadion und Thannhausen, der bis 1757 residierte.',49.891667,10.886944,94710860),(29995575,'Bamberger Dom','Der romanische Bamberger Dom St. Peter und St. Georg gehört zu den deutschen Kaiserdomen und ist mit seinen vier Türmen das beherrschende Bauwerk des Weltkulturerbes Bamberger Altstadt. Er steht auf der markanten Erhebung des Dombergs, der noch weitere historische Gebäude aufweist. Im Inneren befinden sich neben dem Bamberger Reiter das Grab des einzigen heiliggesprochenen Kaiserpaars des Heiligen Römischen Reichs sowie das einzige Papstgrab in Deutschland und nördlich der Alpen. ',49.890833,10.882500,0),(60562989,'Südostfassade','Erwähnenswert sind die ursprünglich 1755 von Johann Anwander geschaffenen Fassadenmalereien, die vielfach restauriert wurden. Nachdem von diesen Bemalungen in den 1950er Jahren nicht mehr viel zu sehen war, wurde durch den Kunstmaler Anton Greiner in den Jahren 1959 bis 1962 eine Neubemalung vorgenommen. Beide Gebäudeseiten sind vollständig mit nachempfundenen allegorischen Szenen und architektonischen Details, der typischen Illusionsmalerei in dieser Zeit, verziert. Kleine, tatsächlich figürlich gestaltete Elemente an der östlichen Seite verstärken den räumlichen Eindruck. Die Rokokobalkons und Wappenreliefs stammen von Jos. Bonaventura Mutschele.',49.891667,10.886944,94710860),(71846253,'St. Lorenz','St. Lorenz ist ein gotischer Kirchenbau in Nürnberg. Die Lorenzkirche war die Pfarrkirche des südlich der Pegnitz gelegenen mittelalterlichen Siedlungskerns der ehemaligen Reichsstadt Nürnberg und bildet städtebaulich das Pendant zu der älteren Kirche St. Sebald im nördlichen Stadtteil. Baubeginn der dreischiffigen Basilika war um 1250, der spätgotische Hallenchor wurde 1477 vollendet.',49.451000,11.078056,0),(88575206,'St. Sebald ','Die mittelalterliche Kirche St. Sebald in Nürnberg, auch Sebalduskirche genannt (nach dem wohl im 8. Jahrhundert in der Gegend von Nürnberg lebenden Einsiedler Sebaldus), ist die älteste Pfarrkirche Nürnbergs und neben der Frauenkirche und der Lorenzkirche eine der herausragenden Kirchenbauten der Stadt.',49.455139,11.075917,0),(92437925,'Weißer Turm','Der Turm war ursprünglich Bestandteil des Inneren Spittlertores (benannt nach dem ehemals benachbarten Elisabethspital) und beherbergt wie der Laufer Schlagturm eine Schlaguhr, die als Teil eines flächendeckenden Netzes von Schlaguhren die etwas komplizierte Nürnberger Uhr verkündete. ',49.450361,11.070667,0),(92657277,'Rottmeisterhäuschen','Das an den Brückenturm angebaute Fachwerkhaus, das Rottmeisterhäuschen, diente den Führern der Wachmannschaften als Unterkunft.',49.891667,10.886944,94710860),(94710860,'Altes Rathaus','Das Alte Rathaus in Bamberg ist eines der bedeutendsten Bauwerke, die die historische Innenstadt prägen. Es befindet sich zwischen Berg- und Inselstadt im linken Regnitzarm. Diese Lage markiert die alte Herrschaftsgrenze zwischen bischöflicher Berg- und bürgerlicher Inselstadt und zeigt deutlich das Machtstreben des Bamberger Bürgertums.',49.891667,10.886944,0),(98266271,'Adamspforte','Die Adamspforte – sie heißt auch Rote Türe – war der Hauptzugang in den Dom. Sie wurde im Alltag zusammen mit der so genannten Gittertür am anderen Ende des Doms genutzt. Die Adamspforte ist das älteste Portal und wurde erst nach der Fertigstellung der benachbarten Gnadenpforte ausgeschmückt. Es handelt sich vermutlich um die letzten Werke der in Reims geschulten Bildhauerwerkstatt. ',49.890833,10.882500,29995575);
/*!40000 ALTER TABLE `building` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-04-02 22:09:19

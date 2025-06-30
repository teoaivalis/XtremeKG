# 📁 triples/

This folder contains all structured triples extracted from flood-related data sources. These triples are later ingested into a knowledge graph to support semantic querying and comparison across events.

---

## 📂 Subfolders

- `triples_from_text/` – Contains `.txt` files with triples extracted from **textual descriptions** of disasters (e.g., ReliefWeb reports).  
- `triples_from_images/` – Contains `.txt` files with triples extracted from **satellite images**, including RGB (visual), NDWI, and NIR types.

Each file corresponds to a single flood event and contains a list of triples in the form:  
```txt
(FL-2025-000045-COD, hasCountry, "Democratic Republic of the Congo")  
(FL-2025-000045-COD, hasISO3, "cod")  
(FL-2025-000045-COD, hasDisasterType, "Flood")  
(FL-2025-000045-COD, hasStatus, "ongoing")  
(FL-2025-000045-COD, hasDate, "2025-04-04T00:00:00+00:00")  
(FL-2025-000045-COD, hasLatitude, -4.03833)  
(FL-2025-000045-COD, hasLongitude, 21.7587)  
(FL-2025-000045-COD, hasGlide, "FL-2025-000045-COD")  
(FL-2025-000045-COD, fatalitiesReported, 165)  
(FL-2025-000045-COD, injuriesReported, 28)  
(FL-2025-000045-COD, displacedPeople, 7000)  
(FL-2025-000045-COD, peopleAffected, 60000)  
(FL-2025-000045-COD, powerOutage, true)  
(FL-2025-000045-COD, waterSupplyCut, true)  
(FL-2025-000045-COD, affectedArea, "Kinshasa, Democratic Republic of the Congo")  
(FL-2025-000045-COD, hasWaters, 1)  
(FL-2025-000045-COD, hasWoods, 5)  
(FL-2025-000045-COD, causedBy, "Heavy rainfall")  
(FL-2025-000045-COD, weatherCause, "Torrential rains")
```
blablalbal

```txt
(FL-2024-000024-DZA, hasndwiimage, FL-2024-000024-DZA-ndwi)
(FL-2024-000024-DZA-ndwi, showsFeature, waterBody)  
(FL-2024-000024-DZA-ndwi, showsFeature, drySurface)  
(FL-2024-000024-DZA-ndwi, hasLandCover, saturatedLand)  
(FL-2024-000024-DZA-ndwi, hasLandCover, bareSoil)  
(FL-2024-000024-DZA-ndwi, hasLandCover, builtUpArea)  
(FL-2024-000024-DZA-ndwi, hasVegetationMoisture, lowMoisture)  
(FL-2024-000024-DZA-ndwi, hasMoistureLevel, highMoisture)  
(FL-2024-000024-DZA-ndwi, showsSignsOf, flooding)  
(FL-2024-000024-DZA-ndwi, includes, waterBody)  
(FL-2024-000024-DZA-ndwi, containsFeature, drySurface)  
(FL-2024-000024-DZA-ndwi, adjacentTo, waterBody)  
(FL-2024-000024-DZA-ndwi, isPartOf, landscape)  
(FL-2024-000024-DZA-ndwi, mayIndicate, floodPresence)  
(FL-2024-000024-DZA-ndwi, likelyRepresents, surfaceWaterDynamics)  
(FL-2024-000024-DZA-ndwi, experiencing, moistureVariation)```

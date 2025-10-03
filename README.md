# Map Rangefinder for War Thunder

This project aims to create a **ballistic calculator** for War Thunder.  
The goal is to **automatically measure distances from player to squad markers** on the minimap using a neural network, most likely with a **YOLO-based approach**.  

## Current Progress

1. Screenshots of the map have been captured and saved as `.png` files.  
2. Screenshots of the minimap have been extracted from the map images.  
3. These images will be **dockerized** and prepared as training data for the neural network.  

## Next Steps

- Prepare the dataset for YOLO training.  
- Train the neural network to detect squad markers and measure distances.  
- Integrate the calculator into a workflow for War Thunder.  

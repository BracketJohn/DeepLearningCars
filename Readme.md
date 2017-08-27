# Car Simulation using Pymunk and Pygame

This Simulation uses Evolutionary Deep Learning via [Googles TensorFlow](https://github.com/tensorflow/tensorflow) to learn how to navigate different tracks, by only reading from 5 Sensors. You are also able to draw these maps yourself. It is inspired by [this YT video by Samuel Arzt](https://www.youtube.com/watch?v=Aut32pR5PQA).

__DISCLAIMER:__ This is in progress and there might still be a lot missing. Current Features:
* Visualization via Pygame+Pymung Integration
* Ability to create and save Maps by drawing them
* Basic Menu Structures
* Select and Load Created Maps into Simulation, mark Startingpoint

__Next Milestone:__ Basic Simulation Logic, i.e. repeating same Scenario a bunch of times.

How to Run:
```
> git clone https://github.com/BracketJohn/DeepLearningCars
> cd DeepLearningCars
> python deepcars
```

ALTERNATIVELY (Installation via Pip)

```
> git clone https://github.com/BracketJohn/DeepLearningCars
> cd DeepLearningCars
> pip install .
> deepcars
```

Please keep in mind that maps will always be saved in `maps`, therefore installing `deepcars` via pip and then launching it, will result in the creation of `maps`.
# Car Simulation using Pymunk and Pygame

This Simulation uses Evolutionary Deep Learning via [Googles TensorFlow](https://github.com/tensorflow/tensorflow) to learn how to navigate different tracks, by only reading from 5 Sensors. You are also able to draw these maps yourself. It is inspired by [this YT video by Samuel Arzt](https://www.youtube.com/watch?v=Aut32pR5PQA).

__DISCLAIMER:__ This is in progress and there might still be a lot missing. Current Features:
* Visualization via Pygame+Pymung Integration
* Ability to create and save Maps by drawing them
* Basic Menu Structures

__Next Milestone:__ Basic Simulation Logic, i.e. selecting map and then repeating same Scenario a bunch of times.

Run it by:
```
> git clone https://github.com/BracketJohn/DeepLearningCars
> cd DeepLearningCars
> python deepcars
```

ALTERNATIVELY

```
> git clone https://github.com/BracketJohn/DeepLearningCars
> cd DeepLearningCars
> pip install .
> deepcars
```

Please keep in mind that maps will always be saved in `deepcars/maps`, therefore installing `deepcars` via pip and then launching it, will result in the creation of `deepcars/maps`.
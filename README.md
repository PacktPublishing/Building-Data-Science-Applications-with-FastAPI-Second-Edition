
### [Packt Conference : Put Generative AI to work on Oct 11-13 (Virtual)](https://packt.link/JGIEY)

<b><p align='center'>[![Packt Conference](https://hub.packtpub.com/wp-content/uploads/2023/08/put-generative-ai-to-work-packt.png)](https://packt.link/JGIEY)</p></b> 
3 Days, 20+ AI Experts, 25+ Workshops and Power Talks 

Code: <b>USD75OFF</b>

# Building Data Science Applications with FastAPI - Second Edition

<a href="https://www.packtpub.com/product/building-data-science-applications-with-fastapi-second-edition/9781837632749?utm_source=github&utm_medium=repository&utm_campaign=9781837632749"><img src="https://content.packt.com/B19528/cover_image_small.jpg" alt="Building Data Science Applications with FastAPI -Second Edition" height="256px" align="right"></a>

This is the code repository for [Building Data Science Applications with FastAPI -Second Edition](https://www.packtpub.com/product/building-data-science-applications-with-fastapi-second-edition/9781837632749?utm_source=github&utm_medium=repository&utm_campaign=9781837632749), published by Packt.

**Develop, manage, and deploy efficient machine learning applications with Python**

## What is this book about?
Building Data Science Applications with FastAPI is the go-to resource for creating efficient and dependable data science API backends. This second edition incorporates the latest Python and FastAPI advancements, along with two new AI projects – a real-time object detection system and a text-to-image generation platform using Stable Diffusion.

This book covers the following exciting features: 
* Explore the basics of modern Python and async I/O programming
* Get to grips with basic and advanced concepts of the FastAPI framework
* Deploy a performant and reliable web backend for a data science application
* Integrate common Python data science libraries into a web backend
* Integrate an object detection algorithm into a FastAPI backend
* Build a distributed text-to-image AI system with Stable Diffusion
* Add metrics and logging and learn how to monitor them

If you feel this book is for you, get your [copy](https://www.amazon.com/dp/B0C9D1QYVX) today!

<a href="https://www.packtpub.com/?utm_source=github&utm_medium=banner&utm_campaign=GitHubBanner"><img src="https://raw.githubusercontent.com/PacktPublishing/GitHub/master/GitHub.png" 
alt="https://www.packtpub.com/" border="5" /></a>


## Instructions and Navigations
All of the code is organized into folders.

The code will look like the following:
```
from fastapi import FastAPI

app = FastAPI()

@app.get("/users/{type}/{id}")
async def get_user(type: str, id: int):
    return {"type": type, "id": id}
```


**Following is what you need for this book:**
This book is for data scientists and software developers interested in gaining knowledge of FastAPI and its ecosystem to build data science applications. 
Basic knowledge of data science and machine learning concepts and how to apply them in Python is recommended.	

With the following software and hardware list you can run all code files present in the book.


### Software and Hardware List

We’ll mainly work with the Python programming language. The first chapter will explain
how to set up a proper Python environment on your operating system. Some examples also involve
running web pages with JavaScript, so you’ll need a modern browser such as Google Chrome or
Mozilla Firefox.
In Chapter 14, we’ll run the Stable Diffusion model, which requires a powerful machine. We recommend
a computer with 16 GB of RAM and a modern NVIDIA GPU to be able to generate good-looking images.
System requirements are mentioned in the following table:

| Software/Hardware                       | Operating System requirements      |
| ------------------------------------    | -----------------------------------|
| Python 3.10+                            | Windows, Mac OS X, and Linux (Any) |                                                            
| Javascript                              | Windows, Mac OS X, and Linux (Any) |


### Related products <Other books you may enjoy>
* Applied Geospatial Data Science with Python [[Packt]](https://www.packtpub.com/product/applied-geospatial-data-science-with-python/9781803238128) [[Amazon]](https://www.amazon.com/dp/B0BJ7GPXMG)

* Building Data Science Solutions with Anaconda [[Packt]](https://www.packtpub.com/product/building-data-science-solutions-with-anaconda/9781800568785) [[Amazon]](https://www.amazon.com/dp/B09X26411W)

## Get to Know the Author
**François Voron**
graduated from the University of Saint-Étienne (France) and the University of Alicante
(Spain) with a master’s degree in machine learning and data mining. A full stack web developer and
a data scientist, François has a proven track record working in the SaaS industry, with a special focus
on Python backends and REST APIs. He is also the creator and maintainer of FastAPI Users, the #1
authentication library for FastAPI, and is one of the top experts in the FastAPI community

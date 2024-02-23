#!/bin/bash
docker run -u=$(id -u $USER):$(id -g $USER) \
	-e DISPLAY=$DISPLAY \
	-v /tmp/.X11-unix:/tmp/.X11-unix:rw \
	-v $(pwd):/app \
	-u root \
	-p 8080:8080 \
	gessource
		   

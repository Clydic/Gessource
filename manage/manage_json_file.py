#! /usr/bin/env python3
#coding: utf-8
import json
from pprint import pprint

def load(filename):
	with open(filename, "r") as file:
		data=json.load(file)
		
	return data

def save(filename,dicc):
	with open(filename, "w") as file:
		json.dump(dicc,file, indent=4)

def main():
	datas=load("description_sort.json")
	pprint(datas["description_sort"].keys())
	for key in datas["description_sort"].keys():
		print(key)


if __name__=="__main__":
	main()



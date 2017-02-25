# yah

This repo will be used to share Python code to get data from Yahoo Finance. Initially we used mongoDB, but now we decided to use a postgreSQL relational database.

## get_sp500_tickers.ps1

Powershell script that scrapes the SP500 wikipedia page and that updates the list of SP500 constituent's tickers

## database_creation_scripts.sql

Use this to create your db objects

## _initialSeed.py

This script is used to perform a one time bulk download and insert of the historical pricing data into our database


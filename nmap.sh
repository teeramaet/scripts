#!/bin/bash

read -p "Enter the target host (IP or domain): " HOST

mkdir -p nmap

echo "Running initial nmap scan..."
sudo nmap -sC -sV -oA nmap/nmap-initial "$HOST"

echo "Running full port scan..."
sudo nmap -p- -oA nmap/nmap-all "$HOST"

echo "Running UDP scan..."
sudo nmap -sU -sC -sV -oA nmap/nmap-udp "$HOST"

echo "Scans completed and saved in the nmap directory."

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 15 22:07:05 2018

@author: hiske
"""
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
import os

xlim = [-4,4]
ylim = [-3,5]
barrier_x = 1
barrier_y = -5
barrier_w = 0.5
barrier_h = 16
pos_source = (xlim[0] -barrier_x)*0.5
pos_drain = (xlim[1]+barrier_x)*0.5
xpos = lambda x: -6*(x+10.52)
ypos = lambda x: x*0.17

I = np.loadtxt('I.txt')
vsd = np.loadtxt('vsd.txt')
vg = np.loadtxt('vg.txt')

def measurement(ax):
    plt.pcolormesh(vg,vsd,I,cmap=plt.cm.gray,vmin=0E-10,vmax=5E-10)
    plt.xlim([-10.97,-10.05])
    plt.ylim([-0.0075,0.0075])
    cbar = plt.colorbar()
    yticks = np.linspace(-0.0075,0.0075,7)
    plt.yticks(yticks,(yticks*1E3))
    xticks = np.linspace(-10.8,-10.2,4)
    plt.xticks(xticks,xticks)
    cticks = np.linspace(0,5E-10,6)
    cbar.set_ticks(cticks)
    cbar.set_ticklabels(cticks*1E9)
    cbar.set_label('Current (nA)')
    plt.xlabel(r'V$_\mathsf{gate}$ (V)')
    plt.ylabel(r'V$_\mathsf{bias}$ (mV)')


def fixed(ax):
    patches = []
    barrier = mpatches.Ellipse([barrier_x,barrier_y],barrier_w,barrier_h,ec='k',fc='0.6',zorder=3)
    patches.append(barrier)
    barrier = mpatches.Ellipse([-barrier_x,barrier_y],barrier_w,barrier_h,ec='k',fc='0.6',zorder=3)
    patches.append(barrier)
    [ax.add_patch(p) for p in patches]
    plt.xlim(xlim)
    plt.ylim(ylim)
    plt.xticks([])
    plt.yticks([])
    
def reservoirs(ax,v):
    patches = []
    bias_w = xlim[1] - barrier_x
    bias_h = 8
    source_level = -bias_h + v*0.5 + bias_h
    source = mpatches.Rectangle([xlim[0],source_level-bias_h],bias_w,bias_h,ec='k',fc='springgreen')
    patches.append(source)
    drain_level = -bias_h - v*0.5 + bias_h
    drain = mpatches.Rectangle([barrier_x,drain_level-bias_h],bias_w,bias_h,ec='k',fc='springgreen')
    patches.append(drain)
    [ax.add_patch(p) for p in patches]
    return([source_level,drain_level])
    
def levels(ax,pg):
    heights = np.array([-5+i+pg for i in range(0,8)])
    heights[-1]+=0.8
    heights[-6]+=0.25
    for h in heights:
        if h < 3:
            plt.plot([-barrier_x,barrier_x],[h,h],color='k')
    return(heights)

def arrows(ax,heights,right_moving,left_moving):
    patches = []
    for height in heights:
        arc = mpatches.Arc([pos_source*0.5,height+0.25],2,1,theta1=20,theta2=160,zorder=5,lw=2,color='darkorange')
        patches.append(arc)
        arc = mpatches.Arc([-pos_source*0.5,height+0.25],2,1,theta1=20,theta2=160,zorder=5,lw=2,color='darkorange')
        patches.append(arc)
        if right_moving:
            arrowhead = mpatches.RegularPolygon([pos_drain-0.4,height+0.5],3,0.2,color='darkorange')
            patches.append(arrowhead)
            arrowhead = mpatches.RegularPolygon([pos_drain-0.4+pos_source,height+0.5],3,0.2,color='darkorange')
            patches.append(arrowhead)
        if left_moving:
            arrowhead = mpatches.RegularPolygon([-(pos_drain-0.4),height+0.5],3,0.2,color='darkorange')
            patches.append(arrowhead)
            arrowhead = mpatches.RegularPolygon([-(pos_drain-0.4+pos_source),height+0.5],3,0.2,color='darkorange')
            patches.append(arrowhead)
    [ax.add_patch(p) for p in patches]
    
    
    
def carriers(ax,heights,sd):
    source,drain = sd
    current = [False]*len(heights)
    style = dict(marker='o', color='k', ms = 8)
    for i,h in enumerate(heights):
        if (h <= drain) is not (h <source):
            current[i] = True
            plt.plot(pos_source,h,**style)
            plt.plot(pos_drain,h,**style)
            plt.plot(0,h,**style)
        elif (h < drain) and (h <source):
            plt.plot(-0,h,**style)
  
    if any(current):
        left_moving = False
        right_moving = False
        if source >= drain:
            right_moving = True
        if drain >= source:
            left_moving = True
        arrows(ax,heights[current],right_moving,left_moving)
  

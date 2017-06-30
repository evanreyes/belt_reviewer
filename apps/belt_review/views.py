# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, HttpResponse
from django.core.urlresolvers import reverse
from django.db.models import Count
from django.contrib import messages
from .models import UserAccount, Book, Author, Review

def index(request):
    if 'logged_in' not in request.session:
        request.session['logged_in'] = False
        return redirect('belt_review:index')
    if request.session['logged_in'] == True:
        return redirect('belt_review:books')
    return render(request, "belt_review/index.html")

def register(request):
    if request.method == "GET":
        return redirect('belt_review:index')
    else:
        if UserAccount.objects.checkReg(request.POST, request):
            validReg = True
            return redirect('belt_review:books')
        else:
            validReg = False
            return redirect('belt_review:index')

def login(request):
    if request.method == "GET":
        return redirect('belt_review:index')
    else:
        if UserAccount.objects.checkLog(request.POST, request):
            validLog = True
            request.session['logged_in'] = True
            return redirect('belt_review:books')
        else:
            validLog = False
            return redirect('belt_review:index')

def books(request):
    context = {
    'books': Book.objects.all().order_by('title'),
    'authors': Author.objects.all(),
    'reviews': Review.objects.all().order_by('-created_at')
    }
    return render(request, "belt_review/books.html", context)

def newbook(request):
    context = {
        'authors': Author.objects.all()
    }
    return render(request, "belt_review/newbook.html", context)

def createbook(request):
    Book.objects.checkBook(request.POST, request)
    return redirect('belt_review:newbook')

def bookinfo(request, id):
    context = {
    'books': Book.objects.get(id=id),
    'reviews': Review.objects.filter(book__id=id).order_by('-created_at')
    }
    return render(request, "belt_review/bookinfo.html", context)


def userprofile(request, id):
    context = {
    'books': Book.objects.all(),
    'users': UserAccount.objects.filter(id=id),
    'user_reviews': Review.objects.filter(user__id=id).count(),
    'reviews': Review.objects.filter(user__id=id)
    }
    return render(request, "belt_review/userprofile.html", context)

def newreview(request, id):
    Book.objects.newReview(request.POST, id, request)
    return redirect('belt_review:bookinfo', id=id)

def deletereview(request, id):
    Review.objects.filter(id=id).delete()
    return redirect('belt_review:books')

def logout(request):
    request.session.clear()
    return redirect('belt_review:index')

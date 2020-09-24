from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .forms import CreateAuction
from .models import User, Auction, Categories, Comments, Bid, WatchList, Closed_case
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Max
from django.contrib import messages


def index(request):
    allData = Closed_case.objects.values_list('itemNumb')
    data = []
    for x in allData:
        data.append(x[0])
        print()
    #choicing the biggest value from the table
    #bidReualt = Bid.objects.order_by("-bidPrice").first()
    #print(bidReualt)
    #top = Bid.objects.order_by('bidPrice').values('userName', 'bidPrice', 'productId').last()
    #print(top)
    print(data)
    newList = []
    newName = []
    for xx in data:
        closed = Bid.objects.filter(productId=xx).latest('bidPrice')
        if str(closed.userName) == str(request.user):
            newList.append(xx)
            newName.append(str(closed.userName))

    print(newList, "Name ", newName)

    data = {'data':Auction.objects.all(), 'dat':data, 'closedBidNum': newList, 'closedBidName': newName}
    return render(request, "auctions/index.html", data)

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def listView(request, listId):
    allData = Closed_case.objects.values_list('itemNumb')
    data = []
    for x in allData:
        data.append(x[0])

    listDetail = Auction.objects.get(pk=listId)
    allComment = Comments.objects.filter(prodId=listId)
    count = Bid.objects.filter(productId=listId)
    totalCount = Bid.objects.filter(productId=listId).count()

    maxAmount = count.aggregate(Max('bidPrice'))
    fimAmt = maxAmount['bidPrice__max']
    data = {'dataDetail':listDetail, 'userComment':allComment, 'finaAmt': fimAmt, 'aucAmt':listDetail.price, 'bid':totalCount, 'dat':data}
    if allComment:
        return render(request, "auctions/index.html", data)
    
    return render(request, "auctions/index.html", data)

@login_required(login_url='login')
def bidId(request, bidId):
    obj = Bid()
    highestPrice = Bid.objects.filter(productId=bidId)
    highPrice = Bid.objects.filter(productId=bidId).count()

    if request.method == "POST":
        if 'Watchlist' in request.POST:
            item_to_save = get_object_or_404(Auction, pk=bidId)
            amoutHigh = highestPrice.aggregate(Max('bidPrice'))
            finalAmount = amoutHigh['bidPrice__max']
            listDetail = Auction.objects.get(pk=bidId)
            allComment = Comments.objects.filter(prodId=bidId)
            acuAmt = Auction.objects.get(pk=bidId)
            if finalAmount:
                data = {'dataDetail':listDetail, 'userComment':allComment, 'bid':highPrice, 'finaAmt': finalAmount}
            else:
                data = {'dataDetail':listDetail, 'userComment':allComment, 'bid':highPrice, 'finaAmt': acuAmt.price}
            

            if WatchList.objects.filter(user=request.user, listItem=bidId).exists():
                messages.add_message(request, messages.INFO, "Already Exists")
                return render(request, "auctions/index.html", data)
            user_list = WatchList(user=request.user)
            user_list.save()
            user_list.listItem.add(item_to_save)
            messages.add_message(request, messages.INFO, "Added to WatchList")
            return render(request, "auctions/index.html", data)
        else:
            listDetail = Auction.objects.get(pk=bidId)
            allComment = Comments.objects.filter(prodId=bidId)
            
            bid = request.POST['quantity']

            try:
                count = Bid.objects.filter(productId=bidId)

                if count:
                    print("Try main IF ")
                    maxAmount = count.aggregate(Max('bidPrice'))

                    if maxAmount['bidPrice__max'] > int(bid):
                        message = "Low Bid $" + bid
                        data = {'dataDetail':listDetail, 'userComment':allComment, 'finaAmt':maxAmount['bidPrice__max'], 'mess':message, 'bid':highPrice}
                        return render(request, "auctions/index.html", data)
                    else:
                        print("Try mini ELSE1 ")
                        obj.userName = request.user
                        obj.bidPrice = bid
                        obj.productId = bidId
                        obj.save()
                        amoutHigh = highestPrice.aggregate(Max('bidPrice'))
                        highPrice = Bid.objects.filter(productId=bidId).count()
                        finalAmount = amoutHigh['bidPrice__max']
                        data = {'dataDetail':listDetail, 'userComment':allComment, 'finaAmt': finalAmount,'bid':highPrice}
                        return render(request, "auctions/index.html", data)
                else:
                    print("Try mani ELSE ")
                    print("Check from ObjectDoesNotExist")
                    message = "Low Bid $" + bid
                    acuAmt = Auction.objects.get(pk=bidId)
                    if int(bid) < acuAmt.price:
                        data = {'dataDetail':listDetail, 'userComment':allComment, 'finaAmt':acuAmt.price, 'mess':message, 'bid':highPrice}
                        return render(request, "auctions/index.html", data)
                    else:
                        print("Try mini else ")
                        obj.userName = request.user
                        obj.bidPrice = bid
                        obj.productId = bidId
                        obj.save()
                        amoutHigh = highestPrice.aggregate(Max('bidPrice'))
                        finalAmount = amoutHigh['bidPrice__max']
                        highPrice = Bid.objects.filter(productId=bidId).count()
                        data = {'dataDetail':listDetail, 'userComment':allComment, 'finaAmt': finalAmount, 'bid':highPrice}
                        return render(request, "auctions/index.html", data)

            except ObjectDoesNotExist:
                acuAmt = Auction.objects.get(pk=bidId)
                print("ObjectDoesNotExist ")
                if int(bid) < int(acuAmt.price):
                    print("ObjectDoesNotExist IF ")
                    message = "Low Bid $" + bid
                    data = {'dataDetail':listDetail, 'userComment':allComment, 'finaAmt':acuAmt.price, 'mess':message, 'bid':highPrice}
                    return render(request, "auctions/index.html", data)
                else:
                    print("ObjectDoesNotExist ELSE ")
                    obj.userName = request.user
                    obj.bidPrice = bid
                    obj.productId = bidId
                    obj.save()
                    amoutHigh = highestPrice.aggregate(Max('bidPrice'))
                    finalAmount = amoutHigh['bidPrice__max']
                    data = {'dataDetail':listDetail, 'userComment':allComment, 'finaAmt': finalAmount}
                    return render(request, "auctions/testing.html", {'mess':amoutHigh})
    return render(request, "auctions/testing.html")

def publish_view(request):
    if request.method == "POST":
        obj = Auction()
        data = CreateAuction(request.POST, request.FILES)
        if data.is_valid():
            title = data.cleaned_data['title']
            discription = data.cleaned_data['discription']
            price = data.cleaned_data['price']
            category = data.cleaned_data['category']
            image = data.cleaned_data['image']

            obj.title = title
            obj.discription = discription
            obj.price = price
            obj.category = category
            obj.image = image
            obj.userName = request.user
            obj.save()
            return HttpResponseRedirect(reverse ("index"))
        return render(request, "auctions/create.html")
    userForm = CreateAuction()
    form = {'userForm':userForm}
    return render(request, "auctions/create.html", form)

@login_required(login_url='login')
def user_comment(request, commId):
    allData = Closed_case.objects.values_list('itemNumb')
    data = []
    for x in allData:
        data.append(x[0])

    acuAmt = Auction.objects.get(pk=commId)
    highestPrice = Bid.objects.filter(productId=commId)
    amoutHigh = highestPrice.aggregate(Max('bidPrice'))
    obj = Comments()
    if request.method == "POST":
        comment = request.POST['comment']
        obj.comments = comment
        obj.userName = request.user
        obj.prodId = commId
        obj.save()
        listDetail = Auction.objects.get(pk=commId)
        allComment = Comments.objects.filter(prodId=commId)
        highPrice = Bid.objects.filter(productId=commId).count()
        if amoutHigh['bidPrice__max'] == None:
            data = {'dataDetail':listDetail, 'userComment':allComment, 'dat':data, 'finaAmt':acuAmt.price, 'bid':highPrice}
            return render(request, "auctions/index.html", data)
        else:
            data = {'dataDetail':listDetail, 'userComment':allComment, 'dat':data, 'finaAmt':amoutHigh['bidPrice__max'], 'bid':highPrice}
            return render(request, "auctions/index.html", data)

def watch_list(request):
    allData = Closed_case.objects.values_list('itemNumb')
    data = []
    for x in allData:
        data.append(x[0])

    watchList = WatchList.objects.filter(user=request.user)
    return render(request, "auctions/index.html", {'watchListdata':watchList, 'dat':data})

def delete_item(request, deletId):
    allData = Closed_case.objects.values_list('itemNumb')
    data = []
    for x in allData:
        data.append(x[0])

    deleteItem = WatchList.objects.filter(user=request.user, listItem=deletId)
    dataItem = deleteItem.get()
    dataItem.delete()
    watchList = WatchList.objects.filter(user=request.user)
    return render(request, "auctions/index.html", {'watchListdata':watchList, 'dat':data})

def display_cate(request, categoryName, idLast):
    allData = Closed_case.objects.values_list('itemNumb')
    dataa = []
    for x in allData:
        dataa.append(x[0])

    data = Auction.objects.filter(category__nameCata = categoryName)
    send = {'categoryName':data, 'dat':dataa}
    return render(request, "auctions/index.html", send)

def myPost(request):
    allData = Closed_case.objects.values_list('itemNumb')
    data = []
    for x in allData:
        data.append(x[0])
    myPost = Auction.objects.filter(userName=request.user)
    return render(request, "auctions/index.html", {'my_list':myPost, 'dat':data })

def close_case(request, closeId):
    value = Closed_case.objects.filter(itemNumb=closeId, itemStat="closed").exists()
    myPost = Auction.objects.filter(userName=request.user)
    allData = Closed_case.objects.values_list('itemNumb')
    data = []
    for x in allData:
        data.append(x[0])
    if request.method == "POST":
        if not value:
            x = Closed_case(userName=request.user, itemNumb=closeId, itemStat="closed")
            x.save()
            allData = Closed_case.objects.values_list('itemNumb')
            data = []
            for x in allData:
                data.append(x[0])
            return render(request, "auctions/index.html", {'my_list':myPost, 'dat':data})
    return render(request, "auctions/index.html", {'my_list':myPost, 'dat':data})












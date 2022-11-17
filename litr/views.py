from itertools import chain

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q

from . import forms, models
from django.shortcuts import render, redirect, get_object_or_404

from .models import UserFollows


@login_required
def home(request):
    reviews = models.Review.objects.select_related("ticket").filter(
        Q(user__in=UserFollows.objects.filter(user=request.user).values("followed_user")) | Q(user=request.user))

    tickets = models.Ticket.objects.filter(
        Q(user__in=UserFollows.objects.filter(user=request.user).values("followed_user")) | Q(user=request.user)
    )

    posts = sorted(chain(reviews, tickets), key=lambda post: post.time_created, reverse=True)

    paginator = Paginator(posts, 5)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {"page_obj": page_obj, "range": range(5)}
    return render(request, 'litr/home.html', context=context)


@login_required
def posts(request):
    reviews = models.Review.objects.select_related("ticket").filter(Q(user=request.user))
    tickets = models.Ticket.objects.filter(Q(user=request.user))

    posts = sorted(chain(reviews, tickets), key=lambda post: post.time_created, reverse=True)

    paginator = Paginator(posts, 5)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {"page_obj": page_obj}
    return render(request, 'litr/posts.html', context=context)


@login_required
def create_ticket(request):
    form = forms.TicketForm()
    if request.method == 'POST':
        form = forms.TicketForm(request.POST, request.FILES)
        ticket = form.save(commit=False)
        ticket.user = request.user
        ticket.save()
        return redirect('home')
    return render(request, 'litr/create_ticket.html', context={'form': form})


@login_required
def edit_ticket(request, ticket_id):
    ticket = get_object_or_404(models.Ticket, id=ticket_id)
    edit_form = forms.TicketForm(instance=ticket)
    if request.method == 'POST':
        edit_form = forms.TicketForm(request.POST, instance=ticket)
        if edit_form.is_valid():
            edit_form.save()
            return redirect('home')

    context = {
        'edit_form': edit_form,
    }
    return render(request, 'litr/modify_ticket.html', context=context)


@login_required
def delete_ticket(request, ticket_id):
    ticket = get_object_or_404(models.Ticket, id=ticket_id)
    if request.method == 'POST':
        if ticket.user == request.user:
            if models.Review.objects.filter(ticket=ticket_id).exists():
                models.Review.objects.filter(ticket=ticket_id).delete()
            else:
                ticket.delete()
                return redirect('posts')
    return render(request, 'litr/delete_ticket.html', {'ticket': ticket})


@login_required
def create_review(request, ticket_id):
    ticket = get_object_or_404(models.Ticket, id=ticket_id)
    review_form = forms.ReviewForm()
    if request.method == 'POST':
        review_form = forms.ReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()
            return redirect('home')

    context = {
        'ticket_form': ticket,
        'review_form': review_form,
    }
    return render(request, 'litr/create_review.html', context=context)


@login_required
def create_review_and_ticket(request):
    ticket_form = forms.TicketForm()
    review_form = forms.ReviewForm()
    if request.method == 'POST':
        ticket_form = forms.TicketForm(request.POST, request.FILES)
        review_form = forms.ReviewForm(request.POST)
        if any([ticket_form.is_valid(), review_form.is_valid()]):
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            review = review_form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()
            return redirect('home')
    context = {
        'ticket_form': ticket_form,
        'review_form': review_form,
    }
    return render(request, 'litr/create_review.html', context=context)


@login_required
def edit_review(request, review_id):
    review = get_object_or_404(models.Review, id=review_id)
    edit_form = forms.ReviewForm(instance=review)
    if request.method == 'POST':
        edit_form = forms.ReviewForm(request.POST, instance=review)
        if edit_form.is_valid():
            edit_form.save()
            return redirect('home')

    context = {
        'edit_form': edit_form,
    }
    return render(request, 'litr/modify_review.html', context=context)


@login_required
def delete_review(request, review_id):
    review = get_object_or_404(models.Review, id=review_id)
    if review.user == request.user:
        if request.method == 'POST':
            review.delete()
            return redirect('posts')
    return render(request, 'litr/delete_review.html', {'review': review})


@login_required
def follow_users(request):
    subscription_list = UserFollows.objects.filter(user=request.user)
    follower_list = UserFollows.objects.filter(followed_user=request.user)
    form = forms.FollowUsersForm(request_user=request.user, former_followed_user=subscription_list)
    if request.method == 'POST':
        form = forms.FollowUsersForm(request.POST, request_user=request.user, former_followed_user=subscription_list)
        if form.is_valid():
            followed = form.cleaned_data.get("followed_user")
            user = request.user
            UserFollows.objects.create(user=user, followed_user=followed)
            return redirect('home')

    context = {
        "form": form,
        "form_subscription": subscription_list,
        "form_followers": follower_list,
    }
    return render(request, 'litr/subscriptions.html', context=context)


@login_required
def unfollow_users(request, subs_id):
    subscription = get_object_or_404(models.UserFollows, id=subs_id)
    if request.method == 'POST':
        subscription.delete()
        return redirect('home')

    return render(request, 'litr/delete_subscription.html', {'subscription': subscription})

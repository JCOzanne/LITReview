from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User

from . import forms, models
from .forms import TicketForm
from .models import Ticket


@login_required
def home(request):
    reviews=models.Review.objects.all()
    tickets=models.Ticket.objects.all()
    return render(request, 'blog/home.html', context={'reviews':reviews, 'tickets':tickets})


@login_required
def create_review(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    form = forms.ReviewForm()

    if request.method == 'POST':
        form = forms.ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.ticket = ticket
            review.user = request.user
            review.save()
            return redirect('home')

    return render(request, 'blog/create_review.html',
                  context={'form': form, 'ticket': ticket})


@login_required
def create_review_and_ticket(request):
    ticket_form = forms.TicketForm()
    review_form = forms.ReviewForm()

    if request.method == 'POST':
        ticket_form = forms.TicketForm(request.POST, request.FILES)
        review_form = forms.ReviewForm(request.POST)

        if ticket_form.is_valid() and review_form.is_valid():
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.save()

            review = review_form.save(commit=False)
            review.ticket = ticket
            review.user = request.user
            review.save()

            return redirect('home')

    return render(request, 'blog/create_review_and_ticket.html',
                  context={'ticket_form': ticket_form,
                           'review_form': review_form})


@login_required
def create_ticket(request):
    form = forms.TicketForm()
    if request.method == 'POST':
        form = forms.TicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect('home')
    return render(request, 'blog/create_ticket.html', context={'form': form})


@login_required
def follow_users(request):
    form = forms.FollowUserForm()
    followed_users = models.UserFollows.objects.filter(user=request.user)

    if request.method == 'POST':
        form = forms.FollowUserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['follows']
            try:
                user_to_follow = get_object_or_404(User, username=username)
                if user_to_follow != request.user:
                    models.UserFollows.objects.get_or_create(
                        user=request.user,
                        followed_user=user_to_follow
                    )
            except Http404:
                messages.error(request, "Utilisateur non trouvé")

    return render(request, 'blog/follow_users.html',
                  {'form': form, 'followed_users': followed_users})


@login_required
def edit_ticket(request, ticket_id):
    ticket = get_object_or_404(models.Ticket, id=ticket_id)

    if request.user != ticket.user:
        messages.error(request, "Vous n'êtes pas autorisé à modifier ce ticket.")
        return redirect('home')

    if request.method == 'POST':
        form = forms.TicketForm(request.POST, request.FILES, instance=ticket)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = forms.TicketForm(instance=ticket)

    return render(request, 'blog/create_ticket.html', {'form': form})

@login_required
def delete_ticket(request, ticket_id):
    ticket = get_object_or_404(models.Ticket, id=ticket_id)

    if request.user != ticket.user:
        messages.error(request, "Vous n'êtes pas autorisé à supprimer ce ticket.")
        return redirect('home')

    if request.method == 'POST':
        ticket.delete()
        return redirect('home')

    return render(request, 'blog/delete_ticket.html', {'ticket': ticket})

@login_required
def edit_review(request, review_id):
    review = get_object_or_404(models.Review, id=review_id)

    if request.user != review.user:
        messages.error(request, "Vous n'êtes pas autorisé à modifier cette critique.")
        return redirect('home')

    if request.method == 'POST':
        form = forms.ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = forms.ReviewForm(instance=review)

    return render(request, 'blog/create_review.html', {'form': form})


@login_required
def delete_review(request, review_id):
    review = get_object_or_404(models.Review, id=review_id)

    if request.user != review.user:
        messages.error(request, "Vous n'êtes pas autorisé à supprimer cette critique.")
        return redirect('home')

    if request.method == 'POST':
        review.delete()
        return redirect('home')

    return render(request, 'blog/delete_review.html', {'review': review})
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.db.models import Q

from . import forms, models
from .models import Ticket

User = get_user_model()


@login_required
def home(request):
    # Récupérer les utilisateurs suivis
    followed_users = models.UserFollows.objects.filter(
        user=request.user,
        is_blocked=False
    ).values_list('followed_user', flat=True)

    # Inclure l'utilisateur connecté
    users_to_show = list(followed_users) + [request.user.id]

    # Récupérer les tickets
    tickets = models.Ticket.objects.filter(
        Q(user__in=users_to_show)
    ).order_by('-time_created')

    # Récupérer les critiques
    reviews = models.Review.objects.filter(
        Q(user__in=users_to_show) |
        Q(ticket__user=request.user)
    ).order_by('-time_created')

    # Combiner et trier les tickets et reviews
    combined_posts = list(tickets) + list(reviews)
    combined_posts.sort(key=lambda x: x.time_created, reverse=True)

    return render(request, 'blog/home.html', {
        'posts': combined_posts
    })


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


@login_required
def follow_users(request):
    followed = models.UserFollows.objects.filter(
        user=request.user,
        is_blocked=False
    )

    blocked = models.UserFollows.objects.filter(
        user=request.user,
        is_blocked=True
    )

    if request.method == 'POST':
        form = forms.FollowUserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            try:
                user_to_follow = User.objects.get(username=username)

                if user_to_follow == request.user:
                    messages.error(request, "Vous ne pouvez pas vous suivre vous-même")
                    return redirect('follow_users')

                existing_follow, created = models.UserFollows.objects.get_or_create(
                    user=request.user,
                    followed_user=user_to_follow
                )

                if created:
                    messages.success(request, f"Vous suivez maintenant {username}")
                else:
                    messages.info(request, f"Vous suivez déjà {username}")

            except User.DoesNotExist:
                messages.error(request, "Utilisateur non trouvé")

    else:
        form = forms.FollowUserForm()

    return render(request, 'blog/follow_users.html', {
        'form': form,
        'followed_users': followed,
        'blocked_users': blocked
    })


@login_required
def unfollow_user(request, username):
    try:
        user_to_unfollow = User.objects.get(username=username)
        follow_relation = models.UserFollows.objects.filter(
            user=request.user,
            followed_user=user_to_unfollow
        )
        follow_relation.delete()
        messages.success(request, f"Vous ne suivez plus {username}")
    except User.DoesNotExist:
        messages.error(request, "Utilisateur non trouvé")

    return redirect('follow_users')


@login_required
def block_user(request, username):
    try:
        user_to_block = User.objects.get(username=username)
        follow_relation, created = models.UserFollows.objects.get_or_create(
            user=request.user,
            followed_user=user_to_block
        )
        follow_relation.is_blocked = True
        follow_relation.save()
        messages.success(request, f"{username} a été bloqué")
    except User.DoesNotExist:
        messages.error(request, "Utilisateur non trouvé")

    return redirect('follow_users')


@login_required
def unblock_user(request, username):
    try:
        user_to_unblock = User.objects.get(username=username)
        follow_relation = models.UserFollows.objects.get(
            user=request.user,
            followed_user=user_to_unblock,
            is_blocked=True
        )
        follow_relation.is_blocked = False
        follow_relation.save()
        messages.success(request, f"{username} a été débloqué")
    except User.DoesNotExist:
        messages.error(request, "Utilisateur non trouvé")

    return redirect('follow_users')
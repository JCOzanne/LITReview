from itertools import chain

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.db.models import F

from . import forms, models

User = get_user_model()

@login_required
def home(request : HttpRequest) -> HttpResponse:
    """
    Display the home feed with tickets and reviews from followed users.
    :param request: HTTP request object.
    :return: HTTP response rendering the home page 'home.html' with combined posts.
    """
    followed_users = models.UserFollows.objects.filter(
        user=request.user,
        is_blocked=False
    ).values_list('followed_user', flat=True)

    tickets = models.Ticket.objects.filter(
        Q(user=request.user) |
        Q(user__in=followed_users)
    ).order_by('-time_created')

    reviews = models.Review.objects.filter(
        Q(user=request.user) |
        Q(ticket__user=request.user) |
        Q(user__in=followed_users)
    ).order_by('-time_created')

    standalone_ticket_ids = reviews.filter(ticket__user=F('user')).values_list('ticket_id', flat=True)
    tickets = tickets.exclude(id__in=standalone_ticket_ids)

    combined_posts = chain(tickets, reviews)
    combined_posts = sorted(combined_posts, key=lambda x: x.time_created, reverse=True)

    for post in combined_posts:
        if isinstance(post, models.Review):
            post.is_response = post.ticket.user == request.user and post.user != request.user
            post.is_standalone = post.ticket.user == post.user

    return render(request, 'blog/home.html', {
        'posts': combined_posts,
    })

@login_required
def create_review(request : HttpRequest, ticket_id : int) -> HttpResponse:
    """
    Create a review in response to an existing ticket.
    :param request: HTTP request object.
    :param ticket_id: ID of the ticket being reviewed.
    :return: HTTP response rendering the review creation page 'create_review.html'.
    """
    ticket = get_object_or_404(models.Ticket, id=ticket_id)

    form = forms.ReviewForm()

    if request.method == 'POST':
        form = forms.ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.ticket = ticket
            review.user = request.user
            review.save()
            messages.success(request, "Critique créée avec succès.")
            return redirect('home')

    return render(request, 'blog/create_review.html', context={'form': form, 'ticket': ticket})


@login_required
def create_review_and_ticket(request):
    """
    Simultaneously create a ticket and a review.
    :param request: HTTP request object.
    :return: HTTP response rendering the combined creation page 'create_review_and_ticket.html'.
    """
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
    """
    Create a ticket
    :param request: HTTP request object.
    :return: HTTP response rendering the ticket creation page 'create_ticket.html'.
    """
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
def my_tickets(request):
    """
    Display the tickets created by the currently logged-in user.
    :param request: HTTP request object.
    :return: HTTP response rendering the ticket page 'my_ticket.html'.
    """
    tickets = models.Ticket.objects.filter(user=request.user).order_by('-time_created')
    return render(request, 'blog/my_tickets.html', {'tickets': tickets})

@login_required
def edit_ticket(request, ticket_id):
    """
    View to handle the editing of an existing ticket.
    :param request: HTTP request object.
    :param ticket_id: The ID of the ticket to be edited.
    :return: HTTP response rendering the  edit ticket page 'edit_ticket.html'.
    """
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
    """
    View to handle the deletion of an existing ticket.
    :param request: HTTP request object.
    :param ticket_id: The ID of the ticket to be deleted.
    :return: HTTP response rendering the  delete ticket page 'delete_ticket.html' with confirmation.
    """
    ticket = get_object_or_404(models.Ticket, id=ticket_id)

    if request.user != ticket.user:
        messages.error(request, "Vous n'êtes pas autorisé à supprimer ce ticket.")
        return redirect('home')

    if request.method == 'POST':
        ticket.delete()
        return redirect('home')

    return render(request, 'blog/delete_ticket.html', {'ticket': ticket})

@login_required
def my_reviews(request):
    """
    Display the reviews created by the currently logged-in user.
    :param request: HTTP request object.
    :return: HTTP response rendering the review page 'my_review.html'.
    """
    reviews = models.Review.objects.filter(user=request.user).order_by('-time_created')
    return render(request, 'blog/my_reviews.html', {'reviews': reviews})

@login_required
def edit_review(request, review_id):
    """
    View to handle the editing of an existing review.
    :param request: HTTP request object.
    :param review_id: The ID of the review to be edited.
    :return: HTTP response rendering the  edit review page 'edit_review.html'.
    """
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
    """
    View to handle the deletion of an existing review.
    :param request: HTTP request object.
    :param review_id: The ID of the review to be deleted.
    :return: HTTP response rendering the delete review page 'delete_review.html' with confirmation.
    """
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
    """
    View to manage the functionality of following, blocking, and displaying users.
    :param request: HTTP request object.
    :return: HTTP response rendering the followers, followed and blocked users page 'follow_users.html'
    """
    followed = models.UserFollows.objects.filter(
        user=request.user,
        is_blocked=False
    ).select_related('followed_user')

    blocked = models.UserFollows.objects.filter(
        user=request.user,
        is_blocked=True
    ).select_related('followed_user')

    blocked_users = models.UserFollows.objects.filter(
        user=request.user,
        is_blocked=True
    ).values_list('followed_user', flat=True)

    followers = models.UserFollows.objects.filter(
        followed_user=request.user,
        is_blocked=False
    ).exclude(user__in=blocked_users)

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
        'blocked_users': blocked,
        'followers': followers  # Liste correctement filtrée
    })



@login_required
def unfollow_user(request : HttpRequest, username : str) -> HttpResponse:
    """
    View to handle unfollowing a user.
    :param request: HTTP request object.
    :param username: The username of the user to unfollow.
    :return: Redirects to the 'follow_users.html' view after unfollowing.
    """
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
    """
    View to handle blocking a user.
    :param request: HTTP request object.
    :param username: The username of the user to block.
    :return: Redirects to the 'follow_users.html' view after blocking.
    """
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
    """
    View to handle unblocking a user.
    :param request: HTTP request object.
    :param username: The username of the user to unblock.
    :return: Redirects to the 'follow_users' view after unblocking.
    """
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
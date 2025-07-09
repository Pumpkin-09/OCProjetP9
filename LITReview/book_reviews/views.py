from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import TicketForm, ReviewForm, SearchUserForm
from django.contrib import messages
from book_reviews.models import Ticket, Review, UserFollows
from django.contrib.auth import get_user_model
from itertools import chain
from django.db.models import CharField, Value

User = get_user_model()


@login_required
def home(request):
    return render(request, "book_reviews/home.html")


@login_required
def search_user(request):
    form = SearchUserForm(request.GET)
    searched = False
    found_user = User.objects.none()
    user_following_objects = [user_following.followed_user for user_following in request.user.following.all()]
    user_follower_objects = [user_follower.user for user_follower in request.user.followed_by.all()]

    if request.method == "GET" and request.GET:
        if form.is_valid():
            searched = True
            user_searched = form.cleaned_data["user_searched"]
            followed_user = request.user.following.values_list('followed_user__id', flat=True)
            found_user = User.objects.filter(username__icontains=user_searched).exclude(id=request.user.id).exclude(id__in=followed_user)
            if not found_user.exists():
                messages.info(request, f"Aucun utilisateur touvé pour : {user_searched}.")

        else:
            searched = True
            messages.error(request, f"Recherche non valide.")

    context = {
        "form": form,
        "found_user": found_user,
        "searched": searched,
        "user_following_objects": user_following_objects,
        "user_follower_objects": user_follower_objects,
        "specific_message": True,
    }
    return render(request, "book_reviews/follow.html", context)


@login_required
def follow_action(request):
    if request.method == "POST":
        action = request.POST.get("action")
        
        if action == "follow":
            follow_user_id = request.POST.get("followed_user_id")
            try:
                followed_user = User.objects.get(id=follow_user_id)
            except:
                messages.error(request, "L'utilisateur n'existe pas.")
                return redirect("manage_users")
            
            if followed_user == request.user:
                messages.error(request, "Vous ne pouvez pas vous suivre vous-même !")
                return redirect("manage_users")

            if UserFollows.objects.filter(user=request.user, followed_user=followed_user).exists():
                messages.info(request, f"Vous suivez déja {followed_user.username} !")
                return redirect("manage_users")

            follow = UserFollows(user= request.user, followed_user=followed_user)
            follow.save()
            messages.success(request, f"Vous suivez maintenant {followed_user.username}.")
            return redirect("manage_users")

        elif action == "unfollow":
            unfollow_user_id = request.POST.get("unfollow_user_id")
            try:
                unfollow_user = User.objects.get(id=unfollow_user_id)
            except:
                messages.error(request, "L'utilisateur n'existe pas.")
                return redirect("manage_users")
            
            UserFollows.objects.filter(user=request.user, followed_user=unfollow_user).delete()
            messages.success(request, f"Vous ne suivez plus {unfollow_user.username}")

    return redirect("manage_users")


@login_required
def create_ticket(request):
    if request.method == "POST":
        form = TicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            messages.success(request, "Votre ticket a été crée !")
            return redirect('home')
    else:
        form = TicketForm()

    return render(request, "book_reviews/create_ticket.html", {"form": form})


@login_required
def update_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)

    if ticket.user != request.user:
        messages.error(request, "Vous n'avez pas la permission de modifier ce billet.")
        return redirect("home")

    if request.method == "POST":
        form = TicketForm(request.POST, request.FILES, instance=ticket)
        if form.is_valid():
            form.save()
            messages.success(request, "Votre billet a été modifié avec succès !")
            return redirect("posts")
        
    else:
        form = TicketForm(instance=ticket)
    
    context = {
        "form":form,
        "ticket": ticket
        }
    
    return render(request, "book_reviews/update_ticket.html", context)


@login_required
def delete_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)

    if ticket.user != request.user:
        messages.error(request, "Vous n'avez pas la permission de supprimer ce billet.")
        return redirect("home")
    
    if request.method == "POST":
        ticket.delete()
        return redirect('posts')

    context = {"ticket": ticket}
    return render(request, "book_reviews/delete_ticket.html", context)


@login_required
def create_review(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)

    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()
            messages.success(request, "Votre critique a été crée !")
            return redirect('home')
    else:
        form = ReviewForm()

    context = {
        "form": form,
        "ticket": ticket
        }

    return render(request, "book_reviews/create_review.html", context)


@login_required
def update_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)

    if review.user != request.user:
        messages.error(request, "Vous n'avez pas la permission de modifier cette critique.")
        return redirect("home")

    if request.method == "POST":
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            messages.success(request, "Votre critique a été modifié avec succès !")
            return redirect("posts")
        
    else:
        form = ReviewForm(instance=review)
        
    context = {
        "form":form,
        "review": review,
        "ticket": review.ticket
        }

    return render(request, "book_reviews/update_review.html", context)


@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)

    if review.user != request.user:
        messages.error(request, "Vous n'avez pas la permission de supprimer cette critique.")
        return redirect("home")
    
    if request.method == "POST":
        review.delete()
        return redirect('posts')

    context = {"review": review}
    return render(request, "book_reviews/delete_review.html", context)


@login_required
def create_ticket_and_review(request):
    ticket_form = TicketForm()
    review_form = ReviewForm()

    if request.method == "POST":
        ticket_form = TicketForm(request.POST, request.FILES)
        review_form = ReviewForm(request.POST)

        if all([ticket_form.is_valid(), review_form.is_valid()]):
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.save()

            review = review_form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()

            messages.success(request, "Billet et critique créés avec succès !")
            return redirect("home")

    context = {
        "ticket_form": ticket_form,
        "review_form": review_form
        }

    return render(request, "book_reviews/create_ticket_and_review.html", context)


@login_required
def display_ticket_review_flux(request):
    followed_user = request.user.following.values_list('followed_user__id', flat=True)

    all_follow_tickets = Ticket.objects.filter(user__id__in=followed_user).annotate(content_type=Value("TICKET", CharField()))
    all_follow_reviews = Review.objects.filter(user__id__in=followed_user).select_related("ticket").annotate(content_type=Value("REVIEW", CharField()))

    all_user_tickets = Ticket.objects.filter(user=request.user).annotate(content_type=Value("TICKET", CharField()))
    all_user_reviews = Review.objects.filter(user=request.user).select_related("ticket").annotate(content_type=Value("REVIEW", CharField()))
    all_reviews_ticket_user = Review.objects.filter(ticket__user=request.user).exclude(user=request.user).select_related("ticket").annotate(content_type=Value("REVIEW", CharField()))
    id_user_tickets = Review.objects.filter(user=request.user).values_list("ticket__id", flat=True)


    flux = sorted(chain(all_follow_tickets, all_follow_reviews, all_user_tickets, all_user_reviews, all_reviews_ticket_user), key=lambda post: post.time_created, reverse=True)

    context = {
        "flux": flux,
        "id_user_tickets": id_user_tickets
        }

    return render(request, "book_reviews/home.html", context)


@login_required
def display_ticket_review_posts(request):
    all_user_tickets = Ticket.objects.filter(user=request.user).annotate(content_type=Value("TICKET", CharField()))
    all_user_reviews = Review.objects.filter(user=request.user).select_related("ticket").annotate(content_type=Value("REVIEW", CharField()))

    posts = sorted(chain(all_user_reviews, all_user_tickets), key=lambda post: post.time_created, reverse=True)
    context = {"posts": posts}
    
    return render(request, "book_reviews/posts.html", context)

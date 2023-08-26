from django.contrib.auth import login, logout, authenticate
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import AddUserForm, LoginForm
from django.shortcuts import render, redirect
from django.views import View
from .models import Method, Result, Sample, Analysis, Position, UserProfile
from django.utils import timezone
from django.db.models import Q


class StartPageView(View):
    def get(self, request):
        return render(request, 'start_page.html')


class AddUserView(View):
    def get(self, request):
        if request.user.is_authenticated:
            logout(request)
        form = AddUserForm()
        return render(request, 'form.html', {'form': form})

    def post(self, request):
        form = AddUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            if form.cleaned_data['password1'] == form.cleaned_data['password2']:
                user.set_password(form.cleaned_data['password1'])
                user.save()

                position_id = form.cleaned_data['position']
                position = Position.objects.get(id=position_id)

                user_profile = UserProfile(user=user, position=position)
                user_profile.save()

                user = authenticate(username=user.username, password=form.cleaned_data['password1'])
                if user is not None:
                    login(request, user)
                return redirect('main-page')
            else:
                form.add_error('password2', 'Hasła nie pasują do siebie')
        return render(request, 'form.html', {'form': form})


class LoginUserView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'form.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(reverse('main-page'))
        else:
            form.add_error(None, "Niepoprawne dane logowania, spróbuj jeszcze raz!")
        return render(request, 'form.html', {'form': form})


class LogoutUserView(View):
    def get(self, request):
        logout(request)
        return redirect('start-page')


class MainPageView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request,"base.html")

class AddMethodView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "method_add_new.html")

    def post(self, request):
        method_name = request.POST.get("name")
        method_description = request.POST.get("description")
        measurement_name = request.POST.get("measurement_name")
        measurement_unit = request.POST.get("measurement_unit")
        procedure = request.POST.get('procedure')
        author = request.user


        if not method_name:
            return render(request, "method_add_new.html", context={"error": "Podaj nazwę metody"})
        if not method_description:
            return render(request, "method_add_new.html", context={"error": "Należy szczegółowo opisać metodę analityczną!"})
        if Method.objects.filter(name=method_name).first():
            return render(request, "method_add_new.html", context={"error": "Metoda już istnieje"})

        new_method = Method.objects.create(
            name=method_name,
            description=method_description,
            measurement_name=measurement_name,
            measurement_unit=measurement_unit,
            procedure=procedure,
            author=author)

        return redirect("method-list")


class MethodListView(LoginRequiredMixin, View):
    def get(self, request):
        methods = Method.objects.all()
        return render(request, "method_list.html", context={"methods": methods})


class DeleteMethodView(LoginRequiredMixin, View):
    def get(self, request, method_id):
        method = Method.objects.get(id=method_id)
        method.delete()
        return redirect('method-list')


class DetailMethodView(LoginRequiredMixin, View):
    def get(self, request, method_id):
        method = Method.objects.get(id=method_id)
        return render(request, 'method_detail.html', context={"method": method})


class ModifyMethodView(LoginRequiredMixin, View):
    def get(self, request, method_id):
        method = Method.objects.get(id=method_id)
        return render(request, 'method_modify.html', context={"method": method})

    def post(self, request, method_id):
        method = Method.objects.get(id=method_id)
        method_name = request.POST.get('name')
        method_description = request.POST.get('description')
        measurement_name = request.POST.get('measurement_name')
        measurement_unit = request.POST.get('measurement_unit')
        procedure = request.POST.get('procedure')

        if not method_name:
            return render(request, "method_add_new.html", context={"error": "Podaj nazwę metody"})
        if not method_description:
            return render(request, "method_add_new.html", context={"error": "Należy szczegółowo opisać metodę analityczną!"})
        if method_name != method.name and Method.objects.filter(name=method_name).first():
            return render(request, "method_add_new.html", context={"error": "Metoda już istnieje"})

        method.name = method_name
        method.description = method_description
        method.measurement_name = measurement_name
        method.measurement_unit = measurement_unit
        method.procedure = procedure
        method.save()
        return redirect("method-list")


class AddSampleView(LoginRequiredMixin, View):
    def get(self, request):
        methods = Method.objects.all()
        return render(request, 'sample_add.html', {'methods': methods})

    def post(self, request):
        sample_name = request.POST.get('sample-name')
        sample_description = request.POST.get('sample-description')
        selected_methods = request.POST.getlist('selected-methods')

        new_sample = Sample.objects.create(name=sample_name, description=sample_description)

        for method_id in selected_methods:
            method = Method.objects.get(pk=method_id)
            new_sample.methods.add(method)

        return redirect(reverse('add-results', kwargs={'sample_id': new_sample.id}))


class AddResultsView(LoginRequiredMixin, View):
    def get(self, request, sample_id):
        sample = Sample.objects.get(pk=sample_id)
        print(sample)
        methods = sample.methods.all()
        print(methods)
        return render(request, 'result_add.html', {'methods': methods, 'sample': sample})

    def post(self, request, sample_id):
        methods = Method.objects.filter(sample__id=sample_id)

        for method in methods:
            comment = request.POST.get('comment_' + str(method.id))
            result_value = request.POST.get('result_' + str(method.id))

            analysis = Analysis.objects.filter(sample_id=sample_id, method=method, result=None).first()

            if analysis and result_value:
                result = Result.objects.create(
                    user=request.user,
                    method=method,
                    comments=comment,
                    result=int(result_value),
                    date_of_analysis=timezone.now()
                )

                analysis.result = result
                analysis.save()

        return redirect('results-list')


class ResultsListView(LoginRequiredMixin, View):

    def get(self, request):
        results = Result.objects.select_related('method', 'analysis__sample').order_by('-date_of_analysis')
        return render(request, 'results_list.html', {'results': results})


class ResultsSearchView(LoginRequiredMixin, View):
    def get(self, request):
        methods = Method.objects.all()
        return render(request, 'results_search.html', {'methods': methods})

    def post(self, request):
        method_id = request.POST.get('method')
        criteria_type = request.POST.get('criteria_type')
        criteria_value = request.POST.get('criteria_value')

        q = Q()

        if method_id:
            q &= Q(method_id=method_id)

        if criteria_type and criteria_value:
            if criteria_type == 'less':
                q &= Q(result__lt=criteria_value)
            elif criteria_type == 'greater':
                q &= Q(result__gt=criteria_value)

        results = Result.objects.select_related('method', 'analysis__sample').filter(q).order_by(
            '-date_of_analysis')

        return render(request, 'results_list.html', {'results': results})





    

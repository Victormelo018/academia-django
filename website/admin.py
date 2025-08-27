from django.contrib import admin
from .models import (
    Plano, Modalidade, Professor, Aluno, Turma, Matricula,
    Exercicio, Treino, TreinoExercicio, Presenca, AvaliacaoFisica, Pagamento
)

@admin.register(Aluno)
class AlunoAdmin(admin.ModelAdmin):
    list_display = ("nome", "email", "cpf", "plano", "ativo")
    list_filter = ("ativo", "plano")
    search_fields = ("nome", "email", "cpf")

@admin.register(Professor)
class ProfessorAdmin(admin.ModelAdmin):
    list_display = ("nome", "email", "cref", "ativo")
    list_filter = ("ativo", "modalidades")
    search_fields = ("nome", "email", "cref")

@admin.register(Turma)
class TurmaAdmin(admin.ModelAdmin):
    list_display = ("nome", "modalidade", "professor", "capacidade", "ativa", "inicio", "fim")
    list_filter = ("ativa", "modalidade", "professor")
    search_fields = ("nome", "dias_semana")

@admin.register(Treino)
class TreinoAdmin(admin.ModelAdmin):
    list_display = ("aluno", "professor", "objetivo", "ativo", "criado_em")
    list_filter = ("ativo", "professor", "aluno")
    search_fields = ("aluno__nome", "objetivo", "professor__nome")

# Registros simples
admin.site.register(Plano)
admin.site.register(Modalidade)
admin.site.register(Matricula)
admin.site.register(Exercicio)
admin.site.register(TreinoExercicio)
admin.site.register(Presenca)
admin.site.register(AvaliacaoFisica)
admin.site.register(Pagamento)

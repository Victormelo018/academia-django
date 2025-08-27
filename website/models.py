from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# 1) Plano (mensal, trimestral, etc.)
class Plano(models.Model):
    nome = models.CharField(max_length=80, unique=True)
    descricao = models.TextField(blank=True)
    preco = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0)])
    duracao_meses = models.PositiveIntegerField(default=1)
    ativo = models.BooleanField(default=True)
    def __str__(self):
        return f"{self.nome} - R${self.preco:.2f}/{self.duracao_meses}m"

# 2) Modalidade (Musculação, Cross, Yoga, Natação...)
class Modalidade(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    descricao = models.TextField(blank=True)
    def __str__(self):
        return self.nome

# 3) Professor
class Professor(models.Model):
    nome = models.CharField(max_length=120)
    email = models.EmailField(unique=True)
    cref = models.CharField(max_length=30, unique=True)
    telefone = models.CharField(max_length=20, blank=True)
    modalidades = models.ManyToManyField(Modalidade, related_name="professores", blank=True)  # M2M
    ativo = models.BooleanField(default=True)
    def __str__(self):
        return f"{self.nome} (CREF {self.cref})"

# 4) Aluno
class Aluno(models.Model):
    nome = models.CharField(max_length=120)
    email = models.EmailField(unique=True)
    cpf = models.CharField(max_length=14, unique=True)
    data_nascimento = models.DateField()
    plano = models.ForeignKey(Plano, on_delete=models.SET_NULL, null=True, blank=True)  # FK
    ativo = models.BooleanField(default=True)
    def __str__(self):
        return f"{self.nome} - {self.cpf}"

# 5) Turma/Aula coletiva
class Turma(models.Model):
    nome = models.CharField(max_length=120)  # ex.: Yoga Manhã
    modalidade = models.ForeignKey(Modalidade, on_delete=models.PROTECT, related_name="turmas")
    professor = models.ForeignKey(Professor, on_delete=models.PROTECT, related_name="turmas")
    capacidade = models.PositiveIntegerField(default=15)
    inicio = models.DateField()
    fim = models.DateField(null=True, blank=True)
    dias_semana = models.CharField(max_length=40, help_text="Ex.: 2ª/4ª/6ª 07:00")
    ativa = models.BooleanField(default=True)
    def __str__(self):
        return f"{self.nome} - {self.modalidade.nome}"

# 6) Matrícula (Aluno em Turma) — ligação N:N via modelo explícito
class Matricula(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name="matriculas")
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE, related_name="matriculas")
    data = models.DateField(auto_now_add=True)
    ativo = models.BooleanField(default=True)
    class Meta:
        unique_together = ("aluno", "turma")
    def __str__(self):
        return f"{self.aluno.nome} em {self.turma.nome}"

# 7) Exercicio (catálogo)
class Exercicio(models.Model):
    nome = models.CharField(max_length=120, unique=True)
    grupo_muscular = models.CharField(max_length=80, blank=True)  # ex.: Peito, Costas, Pernas
    equipamento = models.CharField(max_length=120, blank=True)
    def __str__(self):
        return self.nome

# 8) Treino (prescrito a um aluno)
class Treino(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name="treinos")
    professor = models.ForeignKey(Professor, on_delete=models.SET_NULL, null=True, blank=True)
    objetivo = models.CharField(max_length=120, blank=True)  # ex.: Hipertrofia A/B
    criado_em = models.DateTimeField(auto_now_add=True)
    ativo = models.BooleanField(default=True)
    def __str__(self):
        return f"Treino de {self.aluno.nome} ({'ativo' if self.ativo else 'inativo'})"

# 9) TreinoExercicio (tabela de itens do treino) — M2M via through
class TreinoExercicio(models.Model):
    treino = models.ForeignKey(Treino, on_delete=models.CASCADE, related_name="itens")
    exercicio = models.ForeignKey(Exercicio, on_delete=models.PROTECT)
    series = models.PositiveIntegerField(validators=[MinValueValidator(1)], default=3)
    repeticoes = models.PositiveIntegerField(validators=[MinValueValidator(1)], default=10)
    carga_kg = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(0)], default=0)
    descanso_seg = models.PositiveIntegerField(default=60)
    observacao = models.CharField(max_length=200, blank=True)
    class Meta:
        unique_together = ("treino", "exercicio")
    def __str__(self):
        return f"{self.exercicio.nome} x{self.series} ({self.repeticoes})"

# 10) Presença em aula coletiva
class Presenca(models.Model):
    matricula = models.ForeignKey(Matricula, on_delete=models.CASCADE, related_name="presencas")
    data = models.DateField()
    presente = models.BooleanField(default=True)
    marcado_em = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ("matricula", "data")
    def __str__(self):
        return f"{self.matricula.aluno.nome} em {self.data:%d/%m/%Y} - {'OK' if self.presente else 'Faltou'}"

# 11) Avaliação Física
class AvaliacaoFisica(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name="avaliacoes")
    data = models.DateField()
    peso_kg = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0)])
    altura_m = models.DecimalField(max_digits=3, decimal_places=2, validators=[MinValueValidator(0.5), MaxValueValidator(2.5)])
    percentual_gordura = models.DecimalField(max_digits=4, decimal_places=1, validators=[MinValueValidator(0), MaxValueValidator(70)], blank=True, null=True)
    observacoes = models.TextField(blank=True)
    def imc(self):
        try:
            return float(self.peso_kg) / (float(self.altura_m) ** 2)
        except Exception:
            return None
    def __str__(self):
        return f"Avaliação {self.aluno.nome} - {self.data:%d/%m/%Y}"

# 12) Pagamento do Plano
class Pagamento(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name="pagamentos")
    plano = models.ForeignKey(Plano, on_delete=models.PROTECT)
    referencia = models.CharField(max_length=20, help_text="Ex.: 2025-08 (competência)")
    valor = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0)])
    pago = models.BooleanField(default=False)
    criado_em = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ("aluno", "referencia")
    def __str__(self):
        return f"{self.aluno.nome} - {self.referencia} - R${self.valor:.2f} ({'Pago' if self.pago else 'Pendente'})"

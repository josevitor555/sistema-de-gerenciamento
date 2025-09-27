
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from cloudinary.models import CloudinaryField


class Categoria(models.Model):
    nome = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nome

    @classmethod
    def create_initial_categories(cls):
        categorias_iniciais = ['Eletrônicos', 'Roupas', 'Alimentos', 'Móveis']
        for nome in categorias_iniciais:
            cls.objects.get_or_create(nome=nome)

    @classmethod
    def get_or_create_categoria(cls, nome):
        nome = nome.strip().title()
        return cls.objects.get_or_create(nome=nome)


# Modelo intermediário atualizado com nome correto da tabela
class ProdutoCategoria(models.Model):
    produto = models.ForeignKey('Produto', on_delete=models.CASCADE,null=True)
    categoria = models.ForeignKey('Categoria', on_delete=models.CASCADE,null=True)

    class Meta:
        # managed = True  # Remover esta linha ou definir como False se a tabela já existir e não for gerenciada pelo Django
        pass

    def __str__(self):
        return f"{self.produto.nome} - {self.categoria.nome}"


class Produto(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    marca = models.CharField(max_length=255, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True) 
    # ✅ Agora usa a tabela correta `produto_categoria_rel`
    categorias = models.ManyToManyField(
        Categoria,
        through='ProdutoCategoria',  # Modelo intermediário correto
        related_name='produtos'
    )
    
    quantidade = models.IntegerField(default=1)
    valor = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    imagem = CloudinaryField('imagem', null=True, blank=True)

    adicional = models.CharField(
        max_length=20,
        choices=[('disponivel', 'Disponível'), ('nao_disponivel', 'Não Disponível')],
        default='disponivel'
    )

    def __str__(self):
        return f"{self.nome} - {'Disponível' if self.adicional == 'disponivel' else 'Não Disponível'}"

    @classmethod
    def get_all_products(cls):
        return cls.objects.all().order_by('-id')  # Exibe os mais novos primeiro)

    @classmethod
    def get_produtos_com_adicional(cls):
        return cls.objects.filter(adicional='disponivel')

    @classmethod
    def get_produtos_sem_adicional(cls):
        return cls.objects.filter(adicional='nao_disponivel')

    @classmethod
    def get_produtos_por_status(cls, status=None):
        if status == 'disponivel':
            return cls.objects.filter(adicional='disponivel')
        elif status == 'nao_disponivel':
            return cls.objects.filter(adicional='nao_disponivel')
        else:
            return cls.objects.all()  # Retorna todos os produtos caso o status não seja passado
class Pedido(models.Model):
    produtos = models.ManyToManyField(Produto, through='ItemPedido')

    def total_pedido(self):
        total = sum(item_pedido.quantidade * item_pedido.produto.valor for item_pedido in self.itempedido_set.all())
        return total

    def __str__(self):
        return f'Pedido {self.id}'

class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.IntegerField(default=1)

    def __str__(self):
        return f'{self.quantidade}x {self.produto.nome}'



class UsuarioManager(BaseUserManager):
    def create_user(self, email, nome, password=None):
        if not email:
            raise ValueError('O endereço de e-mail deve ser fornecido')
        email = self.normalize_email(email)
        user = self.model(email=email, nome=nome, is_active=True)  # Adicionando is_active
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, nome, password=None):
        user = self.create_user(email, nome, password)
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True  # Garantindo que esteja ativo
        user.save(using=self._db)
        return user

class Usuario(AbstractBaseUser):
    email = models.EmailField(unique=True)
    nome = models.CharField(max_length=255)
    password = models.CharField(max_length=128)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)  # Adicionado corretamente
    is_superuser = models.BooleanField(default=False)  # Necessário para superusuários

    objects = UsuarioManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nome']

    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

from rest_framework import serializers
from .models import Categoria, Produto

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ['id', 'nome']


class ProdutoSerializer(serializers.ModelSerializer):
    categorias = CategoriaSerializer(many=True, read_only=True)
    imagem = serializers.ImageField(read_only=True) # CloudinaryField retorna uma URL por padrão

    class Meta:
        model = Produto
        fields = [
            'id',
            'nome',
            'descricao',
            'marca',
            'updated_at',
            'categorias',
            'quantidade',
            'valor',
            'imagem',
            'adicional',
        ]

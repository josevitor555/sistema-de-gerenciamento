export interface Category {
    id: number;
    nome: string;
}

export interface Product {
    id: number;
    nome: string;
    descricao: string;
    marca: string;
    updated_at: string; // Ou Date, dependendo de como você vai parsear
    categorias: Category[];
    quantidade: number;
    valor: number;
    imagem: string; // URL da imagem do Cloudinary
    adicional: 'disponivel' | 'nao_disponivel';
}

import type { Product, Category } from '../types/product';

const API_BASE_URL = 'http://localhost:8000/api';

export const fetchCategories = async (): Promise<Category[]> => {
    try {
        const response = await fetch(`${API_BASE_URL}/categorias/`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return await response.json();
    } catch (error) {
        console.error("Erro ao buscar categorias:", error);
        return [];
    }
};

export const fetchProducts = async (categoryId?: number): Promise<Product[]> => {
    try {
        let url = `${API_BASE_URL}/produtos/`;
        if (categoryId) {
            url += `?categoria=${categoryId}`;
        }
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const productsData: Product[] = await response.json();
        return productsData.map(product => ({
            ...product,
            valor: parseFloat(product.valor as any), // Converte a string para number
        }));
    } catch (error) {
        console.error("Erro ao buscar produtos:", error);
        return [];
    }
};

import { useEffect, useState } from 'react';
import { Header } from "@/components/layout/Header";
import { Footer } from "@/components/layout/Footer";
import { ProductGrid } from "@/product/ProductGrid";
import { CartSidebar } from "@/cart/CartSidebar";
import { CartProvider } from "@/context/CartContext";
import type { Product, Category } from "@/types/product";
import { fetchCategories, fetchProducts } from "@/services/api";

export function Home() {
    const [products, setProducts] = useState<Product[]>([]);
    const [categories, setCategories] = useState<Category[]>([]);
    const [activeCategory, setActiveCategory] = useState<number | null>(null); // null para 'todas'
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const loadData = async () => {
            setLoading(true);
            setError(null);
            try {
                const fetchedCategories = await fetchCategories();
                setCategories(fetchedCategories);

                // Corrigindo o tipo do parâmetro para fetchProducts
                const fetchedProducts = await fetchProducts(
                    activeCategory !== null ? activeCategory : undefined
                );
                setProducts(fetchedProducts);
            } catch (err) {
                setError("Falha ao carregar dados. Tente novamente mais tarde.");
                console.error(err);
            } finally {
                setLoading(false);
            }
        };

        loadData();
    }, [activeCategory]); // Recarrega produtos quando a categoria ativa muda

    if (loading) {
        return <div className="flex justify-center items-center min-h-screen text-lg">Carregando...</div>;
    }

    if (error) {
        return <div className="flex justify-center items-center min-h-screen text-red-500 text-lg">Erro: {error}</div>;
    }

    return (
        <CartProvider>
            <div className="app min-h-screen bg-background">
                <Header />

                <main id="main-content" className="py-8" role="main" aria-label="Produtos disponíveis">
                    <ProductGrid
                        products={products}
                        activeCategory={activeCategory}
                        categories={categories}
                        onCategoryChange={setActiveCategory}
                    />
                </main>

                <Footer />
                <CartSidebar />
            </div>
        </CartProvider>
    );
}
import type { Category } from "@/types/product";
import { cn } from "@/lib/utils";

interface CategoryFilterProps {
    categories: Category[];
    activeCategory: number | null; // Alterado para number | null
    onCategoryChange: (categoryId: number | null) => void; // Alterado para number | null
}

export function CategoryFilter({ categories, activeCategory, onCategoryChange }: CategoryFilterProps) {
    const handleKeyDown = (event: React.KeyboardEvent, categoryId: number | null) => {
        if (event.key === 'Enter' || event.key === ' ') {
            event.preventDefault();
            onCategoryChange(categoryId);
        }
    };

    return (
        <div className="flex flex-wrap gap-2 justify-end">
            <button
                key="all"
                onClick={() => onCategoryChange(null)} // Para filtrar por todas as categorias
                onKeyDown={(e) => handleKeyDown(e, null)}
                className={cn(
                    "rounded-full px-8 py-2 transition-all duration-200",
                    activeCategory === null
                        ? "bg-[#70bf2b] text-white"
                        : "text-muted-foreground border-border"
                )}
                aria-label="Filtrar produtos por categoria: Todas"
                aria-pressed={activeCategory === null}
                role="button"
            >
                Todas
            </button>
            {categories.map((category) => (
                <button
                    key={category.id}
                    onClick={() => onCategoryChange(category.id)}
                    onKeyDown={(e) => handleKeyDown(e, category.id)}
                    className={cn(
                        "rounded-full px-8 py-2 transition-all duration-200",
                        activeCategory === category.id
                            ? "bg-[#70bf2b] text-white"
                            : "text-muted-foreground border-border"
                    )}
                    aria-label={`Filtrar produtos por categoria: ${category.nome}`}
                    aria-pressed={activeCategory === category.id}
                    role="button"
                >
                    {category.nome}
                </button>
            ))}
        </div>
    );
}
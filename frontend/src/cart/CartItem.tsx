import { Minus, Plus, Trash2 } from 'lucide-react';
import { Button } from "@/components/ui/button";
import type { CartItem as CartItemType } from "@/types/cart";
import { useCart } from "@/context/CartContext";

interface CartItemProps {
    item: CartItemType;
}

export function CartItem({ item }: CartItemProps) {
    const { updateQuantity, removeFromCart } = useCart();

    const handleIncrement = () => {
        updateQuantity(item.id, item.quantity + 1);
    };

    const handleDecrement = () => {
        updateQuantity(item.id, item.quantity - 1);
    };

    const handleRemove = () => {
        removeFromCart(item.id);
    };

    return (
        <div className="flex items-center space-x-3 py-4 px-4 bg- border-b border-gray-200 last:border-b-0">
            {/* Product Image */}
            <div className="w-16 h-16 rounded-lg overflow-hidden flex-shrink-0">
                <img
                    src={item.product.imagem}
                    alt={item.product.nome}
                    className="w-full h-full object-cover"
                />
            </div>

            {/* Product Details */}
            <div className="flex-1 min-w-0">
                <h4 className="font-medium text-gray-900 truncate">
                    {item.product.nome}
                </h4>
                <p className="text-lg font-semibold text-gray-900 mt-1">
                    R$ {item.product.valor}
                </p>
            </div>

            {/* Quantity Controls */}
            <div className="flex items-center space-x-2">
                <Button
                    size="sm"
                    variant="outline"
                    onClick={handleDecrement}
                    className="h-8 w-8 p-0 rounded-full border-[#70bf2b] text-[#70bf2b] hover:bg-orange-50"
                    aria-label={`Diminuir quantidade de ${item.product.nome}`}
                >
                    <Minus className="h-4 w-4" />
                </Button>

                <span className="w-8 text-center font-medium">
                    {item.quantity}
                </span>

                <Button
                    size="sm"
                    variant="outline"
                    onClick={handleIncrement}
                    className="h-8 w-8 p-0 rounded-full border-[#70bf2b] text-[#70bf2b] hover:bg-orange-50"
                    aria-label={`Aumentar quantidade de ${item.product.nome}`}
                >
                    <Plus className="h-4 w-4" />
                </Button>
            </div>

            {/* Remove Button */}
            <Button
                size="sm"
                variant="ghost"
                onClick={handleRemove}
                className="h-8 w-8 p-0 text-[#70bf2b] hover:bg-red-50"
                aria-label={`Remover ${item.product.nome} do carrinho`}
            >
                <Trash2 className="h-4 w-4" />
            </Button>
        </div>
    );
}
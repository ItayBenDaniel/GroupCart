// components/ProductModal.tsx
import React from 'react';
import { Modal } from 'react-native';
import { StoreProduct } from '../hooks/useHomeScreenData';
import ProductDetails from './ProductDetails';

type Props = {
    visible: boolean;
    product: StoreProduct | null;
    onClose: () => void;
};

export default function ProductModal({ visible, product, onClose }: Props) {
    if (!product) return null;
    console.log("PRODUCT IS ", product)
    console.log("PRODUCT ID IS1", product.id)
    return (
        <Modal visible={visible} animationType="slide" onRequestClose={onClose}>
            <ProductDetails
                product_id={product.id}
                image={{ uri: `http://10.100.102.9:8002/static/icons/${product.item_code}.png` }}
                name={product.name}
                quantity={product.quantity}
                unit_of_measure={product.unit_of_measure}
                price={product.price.toString()}
                oldPrice={(product.price + 5).toString()}
                onClose={onClose}
            />
        </Modal>
    );
}

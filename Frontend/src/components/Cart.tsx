import React, { createContext, useContext, useEffect, useReducer, useState } from "react";
import { Button } from "./ui/button";
import { Input } from "./ui/input";
import { OrderItem } from "@/lib/datatypes";
import apiFetcher from "@/lib/apiFetcher";
import { toast } from "sonner";

type CartItems = {
    [key: string]: {
        cost: number,
        quantity: number
    }
}

type CartActions =
    | { type: 'ADD', payload: { key: string; cost: number; quantity: number } }
    | { type: 'UPDATE', payload: { key: string; cost: number; quantity: number } }
    | { type: 'DELETE', payload: { key: string } }
    | { type : 'CLEAR' }

const CartReducer = (state: CartItems, action: CartActions) => {
    switch (action.type) {
        case 'ADD':
            if (state[action.payload.key])
                return {
                    ...state,
                    [action.payload.key]: {
                        cost: action.payload.cost,
                        quantity: action.payload.quantity + state[action.payload.key].quantity
                    }
                }

            else
                return {
                    ...state,
                    [action.payload.key]: {
                        cost: action.payload.cost,
                        quantity: action.payload.quantity
                    }
                }

        case 'UPDATE':
            const updatedState = {
                ...state,
                [action.payload.key]: {
                    cost: action.payload.cost,
                    quantity: action.payload.quantity
                }
            }

            if (updatedState[action.payload.key].quantity === 0) {
                const { [action.payload.key]: _, ...rest } = updatedState;
                return rest;
            }

            return updatedState;

        case 'DELETE':
            const { [action.payload.key]: _, ...rest } = state;
            return rest;

        case 'CLEAR':
            return {};

        default:
            return state;
    }
}

const cartContext = createContext<{
    state: CartItems;
    dispatch: React.Dispatch<CartActions>;
} | null>(null);

export const CartProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
    const [state, dispatch] = useReducer(CartReducer, {});
    return (
        <cartContext.Provider value={{ state, dispatch }}>
            {children}
        </ cartContext.Provider>
    )
}

export const useCart = () => {
    const context = useContext(cartContext);
    if (!context) throw new Error("Context must be in card provider")
    return context;
}

const CartItemCard = ({ name, quantity, cost }: { name: string, quantity: number, cost: number }) => {
    const { dispatch } = useCart();
    if (name.length > 20) name = name.substring(0, 20);

    const changeQuantity = (e: React.ChangeEvent<HTMLInputElement>) => {
        const newQuantity: number = (e.target.value === '') ? 0 : Number.parseInt(e.target.value);
        
        dispatch({
            type: 'UPDATE',
            payload: {
                key: name,
                quantity: newQuantity,
                cost: cost
            }
        });
    }

    const deleteItem = () => {
        dispatch({
            type : 'DELETE',
            payload : {
                key : name
            }
        })
    }

    return (
        <div key={name} className="w-full h-auto max-h-20 bg-white rounded p-1 border-2 overflow-hidden">
            <div className="w-full h-full flex justify-between items-start">
                <div className="h-full w-1/2">
                    <h3 className="font-bold">{name}</h3>
                    <b>Cost: ₹{cost}</b>
                </div>
                <div className="h-full w-1/2 flex justify-end items-center gap-1">
                    <Input
                        title={quantity.toString()}
                        value={quantity}
                        onChange={changeQuantity}
                        className="w-10 h-10 inline-block" />
                    <Button className="w-10 h-10 m-0 text-[10px] bg-red-600 text-red-200 hover:bg-red-700" onClick={deleteItem}>Delete</Button>
                </div>
            </div>
        </div>
    )
}

export const CartComponent = (): React.ReactNode => {
    const { state, dispatch } = useCart();
    const [totalCost, setTotalCost] = useState<number>(0);
    const [locationPermission, setLocationPermission] = useState<boolean>(false);
    const [orderList, setOrderList] = useState<{name : string, quantity : number, cost : number}[]>([]);

    const handleLocationPermission = () => {
        window.navigator.permissions
        .query({name : 'geolocation'})
        .then(permissionStatus => {
            setLocationPermission(permissionStatus.state === 'granted');
            if(!(permissionStatus.state === 'granted')) toast(
                <span className="text-red-500 font-bold">
                    Enable location to place order!
                </span>
            )

            permissionStatus.onchange = () => {
                if(permissionStatus.state === 'granted') setLocationPermission(true);
                else setLocationPermission(false);   
            }
        })
        .catch(_ => {
            toast(
                <span className="text-red-500 font-bold">
                    Could't read permission status!
                </span>
            )
        })
    }

    useEffect(() => {

        handleLocationPermission();
    }, []);

    useEffect(() => {
        const newOrderList: { name: string; quantity: number; cost: number }[] = [];
        let newTotalCost : number = 0;

        Object.entries(state).forEach(([key, value]) => {
            newTotalCost += value.quantity * value.cost;
            newOrderList.push({
                name: key,
                quantity: value.quantity,
                cost: value.cost,
            });
        });

        setTotalCost(newTotalCost);
        setOrderList(newOrderList);
    }, [state]);

    const placeOrder = async() => { //Saved for later
        if(!locationPermission) {
            toast(<span className="text-red-500 font-bold">Location permission is required!</span>)
            return;
        }

        const orders : OrderItem[] = orderList.map(item => ({name : item.name, quantity : item.quantity}));
        
        window.navigator.geolocation.getCurrentPosition(async location => {
            const geolocation = {
                longitude : location.coords.longitude,
                latitude : location.coords.latitude
            }

            await apiFetcher.addOrder(geolocation, orders)
                .then(res => {
                    if(res.status == 200){
                        toast('Order has been placed');
                        dispatch({type : 'CLEAR'});
                    } else {
                        toast(
                            <span className="text-red-500 font-bold">
                                Couldn't place order!
                            </span>
                        )
                    }
                })
                .catch(_ => {
                    toast(
                        <span className="text-red-500 font-bold">
                            Order couldn't be placed
                        </span>
                    );
                }
            );
        },
        (_) => {
            toast(
                <span className="text-red-500 font-bold">
                    Could't read location!
                </span>
            )
        }
        );
    }

    return (
        <div className="h-full w-80 overflow-hidden rounded-sm p-1 shadow-lg">
            <b className="text-xl">Total Cost : ₹{totalCost.toFixed(2)}</b> <br />
            <Button disabled={!locationPermission} className="my-1" onClick={placeOrder}>Place Order</Button>
            <div className="h-full w-full flex-col px-1 py-2 overflow-x-hidden overflow-y-scroll">
                {
                    orderList.map((item) =>
                        <CartItemCard
                            key={item.name}
                            name={item.name}
                            quantity={item.quantity}
                            cost={item.cost}
                        />
                    )
                }
            </div>
        </div>
    )
}

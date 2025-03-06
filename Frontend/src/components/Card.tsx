import { ChangeEventHandler, useState } from "react";
import { useCart } from "./Cart";
import { Link } from "react-router-dom";
import { Input } from "./ui/input";
import { Button } from "./ui/button";

const Med_Card = ({ name, cost, available, self_url, image }: { name: string, cost: number, available: boolean, self_url: string, image: string }) => {
    const { dispatch } = useCart();
    const [quantity, setQuantity] = useState<number>(0);
    let totalPrice: number = quantity * cost;

    const handleChange: ChangeEventHandler<HTMLInputElement> = (e) => {
        if (e.target.value == '') {
            setQuantity(0);
            return;
        }
        setQuantity(Number.parseInt(e.target.value))
    }

    const addCart = () => {
        if (quantity === 0) return;

        dispatch({
            type: 'ADD',
            payload: {
                key: name,
                cost: cost,
                quantity: quantity
            }
        })
    }

    return (
        <div key={name} className="inline-block w-72 h-96 rounded-lg shadow-sm shadow-blue-950 border-blue-900 border-2 overflow-hidden">
            <div className="w-full h-1/2 rounded-b-lg overflow-hidden shadow-md">
                <img className="w-full h-full" src={image} alt={name} />
            </div>
            <div className="w-full h-1/2 flex justify-between items-center">
                <div className="w-1/2 h-full p-2">
                    <Link to={self_url}>
                        <h3 className="text-blue-900 font-bold text-xl hover:underline cursor-pointer">
                            {
                            (name.length > 10)?
                            name.substring(0, 10) + "..." : 
                            name
                            }
                        </h3>
                    </Link>
                    <p className={"inline-block px-2 rounded-full font-bold text-white " + (
                        (available) ? "bg-green-500" : "bg-red-500"
                    )}>{available ? "Availble" : "Not Available"}</p>
                    <p className="my-2 font-bold text-md">Cost : <span title={cost.toString()} className="text-green-500">₹{cost.toString().substring(0, 8)}</span></p>
                    <label htmlFor={name + "quantity"} className="font-bold block mb-2">Quantity</label>
                    <Input onChange={handleChange} value={quantity} id={name + "quantity"} type="text" />
                </div>
                <div className="w-1/2 h-full p-2">
                    <p className="font-bold block mb-2 text-lg">Total Price</p>
                    <p className="font-bold block text-xl text-green-500">₹{totalPrice.toFixed(2).toString().substring(0, 13)}</p>
                    <Button className="w-24 mt-[calc(100%-66px)]" onClick={addCart}>Add To Cart</Button>
                </div>
            </div>
        </div>
    );
}

export default Med_Card;
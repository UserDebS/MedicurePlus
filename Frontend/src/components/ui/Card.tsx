import { ChangeEventHandler, useContext, useState } from "react";
import { UserContext } from "./Layout";
import { Link } from "react-router-dom";
import { Input } from "./input";
import { Button } from "./button";

const Med_Card = ({ name, cost, available, self_url }: { name: string, cost: number, available: boolean, self_url: string }) => {
    const cart = useContext(UserContext);
    const [quantity, setQuantity] = useState(0);
    const handleChange: ChangeEventHandler<HTMLInputElement> = (e) => {
        setQuantity(Number.parseInt(e.target.value))
    }

    const addCart = () => {
        cart.order_list.push({
            name: name,
            cost: cost * quantity,
            quantity: quantity
        })
    }
    return (
        <div className="h-auto w-56 p-2"> {/* Set fixed dimensions here */}
            <div className="h-full w-full shadow-md p-2 ">
                <Link to={self_url} className="block">
                    <h1 className="text-xl font-semibold">{name}</h1>
                </Link>

                <h2 className="text-md
                    font-bold text-gray-600">₹{cost}</h2>
                <h2 className={`text-sm ${available ? 'text-green-500' : 'text-red-500'}`}>
                    {available ? 'Available' : 'Not Available'}
                </h2>
                <br />
                <b>Quantity : </b>
                <Input
                    className="w-14 inline-block"
                    onChange={handleChange}
                    value={quantity}
                    type="text"
                />
                <Button className="my-2" onClick={addCart}>Add to Cart</Button>
            </div>
        </div>
    );
}

export default Med_Card;
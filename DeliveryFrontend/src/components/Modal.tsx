import { useState } from "react";
import { Input } from "./ui/input";
import { Button } from "./ui/button";

const Modal = ({
    orderId,
    closeHandler,
    handOverHandler
} : {
    orderId : number,
    closeHandler : () => void,
    handOverHandler : (
        orderId : number,
        orderToken : string
    ) => void
}) => {
    const [orderToken, setOrderToken] = useState<string>("");
    return (
        <section className="size-auto p-1 absolute bg-white top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 border-black border rounded-lg">
            <h1 className="w-full text-xl font-bold">
                Enter Order Token
            </h1>
            <Input 
            type="text"
            onChange={e => setOrderToken(e.target.value)}
            value={orderToken}
            placeholder="Order token"/> <br />

            <Button 
            className="bg-red-500 hover:bg-red-400 active:bg-red-600"
            onClick={_ => closeHandler()}>
                Close
            </Button>&nbsp;
            <Button
            onClick={_ => {
                if(orderToken === '') return;

                handOverHandler(orderId, orderToken);
                closeHandler();
            }}
            >
                Hand Over
            </Button>
        </section>
    );
}
 
export default Modal;
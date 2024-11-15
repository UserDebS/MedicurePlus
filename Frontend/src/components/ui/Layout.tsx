import { createContext } from "react";
import Header from "./Header";
import { Outlet } from "react-router";

interface OrderItem {
    name : string,
    quantity : number,
    cost : number
}



interface Cart {
    order_list : OrderItem[]
}

export const UserContext = createContext<Cart>({
    order_list : []
})

const Layout = () => {
    return ( 
        <UserContext.Provider value={{order_list : []}}>
            <div className="h-lvh w-lvw overflow-hidden">
                <Header />
                <main className="h-[calc(100lvh-3.5rem)] overflow-y-auto">
                    <Outlet/>
                </main>
            </div>
        </UserContext.Provider>
     );
}
 
export default Layout;
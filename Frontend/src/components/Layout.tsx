import Header from "./Header";
import { Outlet } from "react-router";
import { CartProvider, CartComponent } from "./Cart";
import { Toaster } from "sonner";

const Layout = () => {
    return ( 
        <CartProvider>
            <Toaster />
            <div className="h-lvh w-lvw overflow-hidden">
                <Header />
                <main className="h-[calc(100lvh-3.5rem)] w-full overflow-hidden flex">
                    <Outlet/>
                    <CartComponent />
                </main>
            </div>
        </CartProvider>
     );
}
 
export default Layout;
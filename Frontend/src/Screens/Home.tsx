import Med_Card from "@/components/Card";
import ImageSearch from "@/components/ImageSearch";
import TextSearch from "@/components/TextSearch";
import GridShowcase from "@/components/ui/GridShowcase";
import apiFetcher from "@/lib/apiFetcher";
import { MedicineDetails } from "@/lib/datatypes";
import { getSignal } from "@/lib/supabaseClient";
import { RealtimeChannel } from "@supabase/supabase-js";
import { useEffect, useRef, useState } from "react";
import { toast } from "sonner";

const Home = () => {
    const [medList, setMedList] = useState<MedicineDetails[]>([]);
    const [offset, setOffset] = useState<number>(0);

    const channelRef = useRef<RealtimeChannel | null> (null);

    const loadInitialData = async() => {
        await apiFetcher.getAllMedicines(offset, 20).then(async(res) =>  {
            const data = await res.json();
            setMedList(data);
        }).catch(_ => console.log(_));
    }

    const addNewData = async() => {
        await apiFetcher.getAllMedicines(offset, 20).then(async(res) =>  {
            const data = await res.json();
            setMedList(prev => {
                const newList = [...prev, ...data]

                return Array.from(new Set(newList.map(item => item.name)))
                    .map(name => newList.find(item => item.name === name));
            });

        }).catch(_ => console.log(_));
    }

    useEffect(() => {
        loadInitialData();
        if(channelRef.current === null) {
            console.log('Setting up channel');
            channelRef.current = getSignal(
                (orderId : number) => {
                    console.log(orderId);
                    apiFetcher.getOrderToken(orderId)
                        .then(res => {
                            if(res.ok) return res.json();
                            else throw new Error('Failed Order token requeust');
                        })
                        .then(res => {
                            toast(
                                <span className="text-green-500 font-bold">
                                    <strong>Order Token</strong> <br />
                                    <span className="text-black">{res}</span>
                                </span>
                            );
                        })
                        .catch(_ => console.log(_));
                }
            );
            console.log(channelRef.current);
        }
    }, []);

    useEffect(() => {
        addNewData();
    }, [offset]);

    return ( 
        <div className="w-full h-full overflow-hidden p-2">
            <div className="w-full h-16 flex justify-end items-center shadow-md rounded-t gap-1 p-2">
                <TextSearch callback={setMedList}/>
                <ImageSearch callback={setMedList} />
            </div>
            <div className="w-full h-[calc(100%-4rem)]">
                <GridShowcase setOffset={setOffset}>
                {
                    medList?.map(data => <Med_Card
                        key={data.name}
                        name={data.name}
                        cost={data.cost}
                        available={data.available}
                        self_url={data.self_url}
                        image={data.image}
                    />)
                }
                </GridShowcase>
            </div>
        </div>
     );
}
 
export default Home;
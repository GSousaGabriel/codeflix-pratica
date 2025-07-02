interface Category{
    id:string;
    namne:string;
    is_active:boolean;
    created_at:string;
    updated_at:string;
    deleted_at:null | string;
    description:null | string;
}

export const initialState = {
    categories: [
        category
    ]
}
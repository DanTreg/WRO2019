
export function getBp(){
    fetch("http://localhost:9000/read_json",{
        method:'GET'
    })
        .then(res => {return(res)});
};


export function createNewBp(){
    fetch("http://localhost:9000/read_json",{
        method:'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            r:false,
            g:false,
            w:false,
            y:false,
            b:false
        })
    })
        .then(res => {return(res)});
};
export default createNewBp;
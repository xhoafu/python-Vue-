import axios from "@/api/axios";


export const playlist = () => {
    return axios.get("playlist/playlists/");
  };

export const playlistage = () => {
    return axios.get("playlist/playlists/page_info/")
}

export const playlistDetail = (data) => {
  return axios.get(`playlist/playlists/${data}/`);
};

export const playlistrecommended = () => {
  return axios.get("playlist/playlists/recommended/");
};

export const playlistcollet =(playlist_id) =>{
  return axios.post(`/playlist/playlists/${playlist_id}/collect/`)
}

export const playlistuncollet =(playlist_id) =>{
  return axios.post(`/playlist/playlists/${playlist_id}/uncollect/`)
}
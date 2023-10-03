export type PlaylistQueryParams = {
    key: string,
    part: string,
    playlistId: string,
    maxResults: number,
    pageToken?: string
}

export type _PlaylistItemSnippet = {
    publishedAt: string,
    channelId: string,
    title: string,
    description: string,
    thumbnails: {},
    channelTitle: string,
    videoOwnerChannelTitle: string,
    videoOwnerChannelId: string,
    playlistId: string,
    position: number,
    resourceId: {},
    contentDetails: {},
    status: {}
}

export type _PlaylistItem = {
    id: string,
    snippet:  _PlaylistItemSnippet,
    [key: string]: unknown
}

export type PlaylistItemsPage = {
    id: string, 
    nextPageToken?: string,
    prevPageToken?: string,
    pageInfo: {},
    items: _PlaylistItem[],
    [key: string]: unknown
}

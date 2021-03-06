import os
import cv2
import math
import pdb
import pickle
import numpy as np
import glob as glob
from scipy.sparse import csr_matrix
from scipy.io import loadmat,savemat
from scipy.sparse.csgraph import connected_components
import matplotlib.pyplot as plt



def adj_gaussian_element(sxdiff, sydiff, mdis,SBS,useSBS = True):
    sigma_xspd_diff = 0.7
    sigma_yspd_diff = 0.7
    sigma_spatial_distance = 200
    if useSBS:
        adj_element = np.exp((-sxdiff**2/sigma_xspd_diff**2)+(-sydiff**2/sigma_yspd_diff**2)+(-mdis**2/sigma_spatial_distance**2) + SBS)
    else:
        adj_element = np.exp((-sxdiff**2/sigma_xspd_diff**2)+(-sydiff**2/sigma_yspd_diff**2)+(-mdis**2/sigma_spatial_distance**2))
    # if math.isnan(adj_element):
    #     pdb.set_trace()
    return adj_element


def adj_cosine_element(i_trj,j_trj):
    # cosine similarity
    cos_element = np.dot(i_trj,j_trj)/np.sqrt(sum(abs(i_trj)**2))/np.sqrt(sum(abs(j_trj)**2))
    cos_element = (cos_element+1)/2 # make them all positive  
    # print "cos_element: ", str(cos_element)
    if math.isnan(cos_element):
        pdb.set_trace()
    return cos_element


def adj_thresholding_element(sxdiff, sydiff,mdis,dataSource):
    # dth     = 300 #30*1.5
    # yspdth  = 0.7 #0.9 for warpped #5 #y speed threshold
    # xspdth  = 0.7 #0.9 for warpped #5 #x speed threshold

    if dataSource =='Johnson':
        # dth    = 80
        # yspdth = 0.2 #filtered out 2/3 pairs
        # xspdth = 0.35 
        dth    = param_dist
        yspdth = param_yspeed 
        xspdth = param_xspeed



    if (sxdiff <xspdth ) & (sydiff<yspdth ) & (mdis < dth):
        adj_element = 1
        # adj[i,j] = construct_adj(sxdiff, sydiff, mdis)
        """visualize the neighbours"""
        # lines = ax.plot(x[i,idx], y[i,idx],color = (color[i-1].T)/255.,linewidth=2)
        # lines = ax.plot(x[j,idx], y[j,idx],color = (color[j-1].T)/255.,linewidth=2)
        # fig888.canvas.draw()
        # plt.pause(0.0001)
    else:
        adj_element = 0
    return adj_element


# same blob score (SBS) for two trajectories
def sameBlobScore(fgBlobInd1,fgBlobInd2):
    SBS = np.sum(fgBlobInd1 == fgBlobInd2)
    return SBS




def prepare_input_data(isAfterWarpping,isLeft,dataSource):
    if isAfterWarpping:
        if isLeft:
            matPath  = '../DoT/CanalSt@BaxterSt-96.106/leftlane/'
            matfiles = sorted(glob.glob(matPath +'warpped_'+'*.mat'))
            savePath = '../DoT/CanalSt@BaxterSt-96.106/leftlane/adj/'
        else:
            matPath  = '../DoT/CanalSt@BaxterSt-96.106/rightlane/'
            matfiles = sorted(glob.glob(matPath +'warpped_'+'*.mat'))
            savePath = '../DoT/CanalSt@BaxterSt-96.106/rightlane/adj/'
    else:
        if dataSource == 'DoT':
            """for linux"""
            matfilepath = '/media/My Book/CUSP/AIG/DoT/CanalSt@BaxterSt-96.106/CanalSt@BaxterSt-96.106_2015-06-16_16h03min52s762ms/klt/filtered/'
            savePath    = '/media/My Book/CUSP/AIG/DoT/CanalSt@BaxterSt-96.106/CanalSt@BaxterSt-96.106_2015-06-16_16h03min52s762ms/adj/'
            """for mac"""
            # matfilepath   = '../DoT/CanalSt@BaxterSt-96.106/mat/CanalSt@BaxterSt-96.106_2015-06-16_16h03min52s762ms/filtered/'
            # savePath      = '../DoT/CanalSt@BaxterSt-96.106/adj/CanalSt@BaxterSt-96.106_2015-06-16_16h03min52s762ms/'
        if dataSource == 'Johnson':
            """Jay & Johnson"""
            matfilepath = outputPath+'filtered/'
            savePath    = outputPath+'adj/'
            # matfilepath = '../tempFigs/roi2/filtered/'
            # savePath    = '../tempFigs/roi2/' 
        
        matfiles = sorted(glob.glob(matfilepath + 'len*.mat'))
        #matfiles = matfiles[33:]
    return matfiles,savePath



# def trjcluster(useSBS,dataSource):
if __name__ == '__main__':
    isAfterWarpping = False
    isLeft          = False
    useSBS          = False
    dataSource      = 'Johnson'

    matfiles,savePath = prepare_input_data(isAfterWarpping,isLeft,dataSource)
    # adj_element = np.nan
    adj_element = "Thresholding"
    # adj_element = "Gaussian"
    # adj_element = "Cosine"

    # """to visualize the neighbours"""
    fig888 = plt.figure()
    ax     = plt.subplot(1,1,1)

    for matidx,matfile in enumerate(matfiles):
        print "Processing truncation...", str(matidx+1)
        ptstrj = loadmat(matfile)
        ptsidx = ptstrj['trjID'][0]
        x      = csr_matrix(ptstrj['xtracks'], shape=ptstrj['xtracks'].shape).toarray()
        y      = csr_matrix(ptstrj['ytracks'], shape=ptstrj['ytracks'].shape).toarray()
        t      = csr_matrix(ptstrj['Ttracks'], shape=ptstrj['Ttracks'].shape).toarray()
        xspd   = csr_matrix(ptstrj['xspd'], shape=ptstrj['xspd'].shape).toarray()
        yspd   = csr_matrix(ptstrj['yspd'], shape=ptstrj['yspd'].shape).toarray()
        
        if useSBS:
            FgBlobIndex   = csr_matrix(ptstrj['fg_blob_index'], shape=ptstrj['fg_blob_index'].shape).toarray()
            FgBlobIndex[FgBlobIndex==0]=np.nan
        else:
            FgBlobIndex = []


        Numsample = ptstrj['xtracks'].shape[0]
        fnum      = ptstrj['xtracks'].shape[1]


        color         = np.array([np.random.randint(0,255) for _ in range(3*int(Numsample))]).reshape(Numsample,3)
        NumGoodsample = len(x)
        # construct adjacency matrix
        print'building adj mtx ....', NumGoodsample,'*',NumGoodsample
        adj = np.zeros([NumGoodsample,NumGoodsample])
        SBS = np.zeros([NumGoodsample,NumGoodsample])
        num = np.arange(fnum)

        # spdYdiff_file = open('sydiffAll.txt', 'wb')

        # sxdiffAll = []
        # sydiffAll = []
        # mdisAll = []
        # build adjacent mtx
        for i in range(NumGoodsample):
            print "i", i
            # plt.cla()
            for j in range(i, min(NumGoodsample,i+1000)):
                tmp1 = x[i,:]!=0
                tmp2 = x[j,:]!=0
                idx  = num[tmp1&tmp2]
                if len(idx)>param_ovlpframes: # has overlapping
                # if len(idx)>=30: # at least overlap for 100 frames
                    sidx   = idx[0:-1] # for speed
                    sxdiff = np.mean(np.abs(xspd[i,sidx]-xspd[j,sidx]))
                    sydiff = np.mean(np.abs(yspd[i,sidx]-yspd[j,sidx]))                    
                    mdis   = np.mean(np.abs(x[i,idx]-x[j,idx])+np.abs(y[i,idx]-y[j,idx])) #mahhattan distance

                    # sxdiffAll.append(sxdiff)
                    # sydiffAll.append(sydiff)
                    # mdisAll.append(mdis)

                    trj1     = [x[i,idx],y[i,idx]]
                    trj2     = [x[j,idx],y[j,idx]]
                    """counting the sharing blob numbers of two trjs"""
                    if useSBS:
                        SBS[i,j] = sameBlobScore(np.array(FgBlobIndex[i,idx]),np.array(FgBlobIndex[j,idx]))
                    if adj_element =="Thresholding":
                        adj[i,j] = adj_thresholding_element(sxdiff,sydiff,mdis,dataSource)

                    if adj_element =="Gaussian":
                        adj[i,j] = adj_gaussian_element(sxdiff, sydiff, mdis,SBS[i,j],useSBS)

                    if adj_element == "Cosine":
                        i_trj    = np.concatenate((x[i,idx], xspd[i,sidx],y[i,idx],yspd[i,sidx]), axis=1)
                        j_trj    = np.concatenate((x[j,idx], xspd[j,sidx],y[j,idx],yspd[j,sidx]), axis=1)
                        adj[i,j] = adj_cosine_element(i_trj,j_trj)
                else: # overlapping too short
                    if i==j:
                        if useSBS:
                            SBS[i,j] =  sameBlobScore(np.array(FgBlobIndex[i,idx]),np.array(FgBlobIndex[j,idx]))
                        adj[i,j] =  adj_gaussian_element(0, 0, 0,SBS[i,j],useSBS)
                    else:
                        SBS[i,j] = 0
                        adj[i,j] = 0
        # pickle.dump( sxdiffAll, open( './roi2_xspdiff'+str(matidx)+'.p', "wb" ) )
        # pickle.dump( sydiffAll, open( './roi2_yspdiff'+str(matidx)+'.p', "wb" ) )
        # pickle.dump( mdisAll, open( './roi2_mdis'+str(matidx)+'.p', "wb" ) )

        SBS = SBS + SBS.transpose()
        np.fill_diagonal(SBS, np.diagonal(SBS)/2)

        adj = adj + adj.transpose() #add diag twice
        np.fill_diagonal(adj, np.diagonal(adj)/2)

        if useSBS:
            temp = np.multiply(adj.transpose(),(1/np.diagonal(adj)))
            adj_new = temp.transpose()
            adj_new = adj_new + adj_new.transpose() #add diag twice
            np.fill_diagonal(adj_new, np.diagonal(adj_new)/2)
            adj_new[adj_new<10**(-4)]=0
        else:
            adj_new = adj
        
        # pdb.set_trace()
        print "saving adj..."
        # print "use adj_new......"
        sparsemtx = csr_matrix(adj_new)
        s,c       = connected_components(sparsemtx) #s is the total CComponent, c is the label
        result    = {}
        result['adj']     = sparsemtx
        result['c']       = c
        result['trjID']   = ptsidx
        result['xtracks'] = x       
        result['ytracks'] = y
        result['Ttracks'] = t
        result['xspd']    = xspd
        result['yspd']    = yspd

        # pdb.set_trace()
        if not isAfterWarpping:
            # savename = os.path.join(savePath,adj_element+'_Adj_'+matfiles[matidx][-7:-4].zfill(3))
            savename = os.path.join(savePath,adj_element+'_Adj_500_5_1_'+matfiles[matidx][-7:-4].zfill(3))

            savemat(savename,result)
        else:
            savename = os.path.join(savePath,'warpped_Adj_'+str(matidx+1).zfill(3))
            savemat(savename,result)
            

        # """ visualization """
        # pdb.set_trace()        
        # s111,c111 = connected_components(sparsemtx) #s is the total CComponent, c is the label
        # color     = np.array([np.random.randint(0,255) for _ in range(3*int(s111))]).reshape(s111,3)
        # fig888    = plt.figure(888)
        # ax        = plt.subplot(1,1,1)
        # # im = plt.imshow(np.zeros([528,704,3]))
        # for i in range(s111):
        #     ind = np.where(c111==i)[0]
        #     print ind
        #     for jj in range(len(ind)):
        #         startlimit = np.min(np.where(x[ind[jj],:]!=0))
        #         endlimit = np.max(np.where(x[ind[jj],:]!=0))
        #         # lines = ax.plot(x[ind[jj],startlimit:endlimit], y[ind[jj],startlimit:endlimit],color = (0,1,0),linewidth=2)
        #         lines = ax.plot(x[ind[jj],startlimit:endlimit], y[ind[jj],startlimit:endlimit],color = (color[i-1].T)/255.,linewidth=2)
        #         fig888.canvas.draw()
        #     plt.pause(0.0001) 
        # pdb.set_trace()






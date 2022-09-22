from gimpfu import *

def create_guides(theImage, tdrawable, hsplit=0, vsplit=0, make_centre=True, draw_borders=False):
    pdb.gimp_image_undo_group_start(theImage)
    vsplit = int(vsplit) # pf_adjustment returns floats
    hsplit = int(hsplit)
    for i in range(vsplit-1): # cutting thirds only requires two lines
        guide = theImage.width/vsplit * (i+1) 
        pdb.gimp_image_add_vguide(theImage, guide)
        
    for i in range(hsplit-1): 
        guide = theImage.height/hsplit * (i+1)
        pdb.gimp_image_add_hguide(theImage, guide)
    
    if make_centre:        
        pdb.gimp_image_add_vguide(theImage, theImage.width/2)
        pdb.gimp_image_add_hguide(theImage, theImage.height/2)
        
    if draw_borders:
        pdb.gimp_image_add_vguide(theImage, 0)
        pdb.gimp_image_add_hguide(theImage, 0)
        pdb.gimp_image_add_vguide(theImage, theImage.width)
        pdb.gimp_image_add_hguide(theImage, theImage.height)
        
    pdb.gimp_image_undo_group_end(theImage)

register(
 "Ham-Quick-Guides", #Name
    "", #Blurb
    "Create guides for rule of thirds/fourths etc..", #help
    "hamsolo474", #Author
    "MIT Licence", #Copyright
    "2022", #Date
    "<Image>/Image/Guides/Quick Guides", #Menu path
    "",      # image types
    [ # Gui Params
        (PF_ADJUSTMENT, "hsplit", "Horizontal Splits", 3,(1,100,1)),
        (PF_ADJUSTMENT, "vsplit", "Vertical Splits", 3,(1,100,1)),
        (PF_TOGGLE, "make_centre", "Draw centered guides", True),
        (PF_TOGGLE, "borders", "Draw guides on canvas borders", False)
    ],
    [], # Results
    create_guides) #function

main()

def TrackProb(bbfile, ccfile, qqfile, d0Output, z0Output):

	fbb = ROOT.TFILE(bbfile, "READ")
	fcc = ROOT.TFILE(ccfile, "READ")
	fqq = ROOT.TFILE(qqfile, "READ")

	ntbb = fbb.Get("tracks")
	ntcc = fcc.Get("tracks")
	ntqq = fqq.Get("tracks")

	print "Creating " + d0Output
	fd0 = ROOT.TFile(d0Output, "recreate") # may need to be "RECREATE"

	hbd0 = ROOT.TH1F("hb","hb",38,-1.8,2)
	hcd0 = ROOT.TH1F("hc","hc",38,-1.8,2)
	hqd0 = ROOT.TH1F("hq","hq",38,-1.8,2)
	ha0d0 = ROOT.TH1F("ha0","ha0",38,-1.8,2)

	hbpd0 = ROOT.TH1F("hbp","hbp",38,-1.8,2)
	hcpd0 = ROOT.TH1F("hcp","hcp",38,-1.8,2)
	hqpd0 = ROOT.TH1F("hqp","hqp",38,-1.8,2)
	ha0pd0 = ROOT.TH1FTH1F("ha0p","ha0p",38,-1.8,2)

	hbnd0 = ROOT.TH1F("hbn","hbn",38,-1.8,2)
	hcnd0 = ROOT.TH1F("hcn","hcn",38,-1.8,2)
	hqnd0 = ROOT.TH1F("hqn","hqn",38,-1.8,2)
	ha0nd0 = ROOT.TH1F("ha0n","ha0n",38,-1.8,2)

	hbipd0 = ROOT.TH1F("hbip","hbip",200,-5,5)
	hcipd0 = ROOT.TH1F("hcip","hcip",200,-5,5)
	hqipd0 = ROOT.TH1F("hqip","hqip",200,-5,5)

	hjprobd0 = ROOT.TH1F("hjprob","hjprob",50,0,5)
	hjprob2d0 = ROOT.TH1F("hjprob2","hjprob2",195,5,200)

	# hb/hc/hq/ha0
	ntbb.Project("hb", "log10(abs(sd0))","abs(sd0sig)>5")
	ntcc.Project("hc", "log10(abs(sd0))","abs(sd0sig)>5")
	ntqq.Project("hq", "log10(abs(sd0))","abs(sd0sig)>5")

	ha0d0.Add(hbd0)
	ha0d0.Add(hcd0)
	ha0d0.Add(hqd0)

	# normalize
	hbd0.Divide(ha0d0)
	hcd0.Divide(ha0d0)
	hqd0.Divide(ha0d0)

	print "hb/hc/hq written." 

	# hbp/hcp/hqp/ha0p
	ntbb.Project("hbp", "log10(sd0)","abs(sd0sig)>5&&sd0>0")
	ntcc.Project("hcp", "log10(sd0)","abs(sd0sig)>5&&sd0>0")
	ntqq.Project("hqp", "log10(sd0)","abs(sd0sig)>5&&sd0>0")

	ha0pd0.Add(hbpd0)
	ha0pd0.Add(hcpd0)
	ha0pd0.Add(hqpd0)

	# normalize
	hbpd0.Divide(ha0pd0)
	hcpd0.Divide(ha0pd0)
	hqpd0.Divide(ha0pd0)

	print "hbp/hcp/hqp written." 

	# hbn/hcn/hqn/ha0n
	ntbb.Project("hbn", "log10(-sd0)","abs(sd0sig)>5&&sd0<0")
	ntcc.Project("hcn", "log10(-sd0)","abs(sd0sig)>5&&sd0<0")
	ntqq.Project("hqn", "log10(-sd0)","abs(sd0sig)>5&&sd0<0")

	ha0nd0.Add(hbnd0)
	ha0nd0.Add(hcnd0)
	ha0nd0.Add(hqnd0)

	# normalize
	hbnd0.Divide(ha0nd0)
	hcnd0.Divide(ha0nd0)
	hqnd0.Divide(ha0nd0)

	print "hbn/hcn/hqn written." 

	# hbip/hcip/hqip not normalized
	ntbb.Project("hbip", "sd0sig","abs(sd0sig)<5")
	ntcc.Project("hcip", "sd0sig","abs(sd0sig)<5")
	ntqq.Project("hqip", "sd0sig","abs(sd0sig)<5")

	print "hbip/hcip/hqip written." 

	ntqq.Project("hjprob", "abs(sd0sig)","jprobcut>0")
	ntqq.Project("hjprob2", "abs(sd0sig)","jprobcut>0")

	integ = hjprobd0.Integral(0,50) + hjprob2d0.Integral(0,195)
	hjprobd0.Scale(1./integ)
	hjprob2d0.Scale(1./integ)

	print "hjprob/hjprob2 written." 

	fd0.Write();
	fd0.Close();

	print "Creating " + z0Output 
	fz0 = ROOT.TFile(z0Output,"recreate")

	hbz0 = ROOT.TH1F("hb","hb",38,-1.8,2)
	hcz0 = ROOT.TH1F("hc","hc",38,-1.8,2)
	hqz0 = ROOT.TH1F("hq","hq",38,-1.8,2)
	ha0z0 = ROOT.TH1F("ha0","ha0",38,-1.8,2)

	hbpz0 = ROOT.TH1F("hbp","hbp",38,-1.8,2)
	hcpz0 = ROOT.TH1F("hcp","hcp",38,-1.8,2)
	hqpz0 = ROOT.TH1F("hqp","hqp",38,-1.8,2)
	ha0pz0 = ROOT.TH1F("ha0p","ha0p",38,-1.8,2)

	hbnz0 = ROOT.TH1F("hbn","hbn",38,-1.8,2)
	hcnz0 = ROOT.TH1F("hcn","hcn",38,-1.8,2)
	hqnz0 = ROOT.TH1F("hqn","hqn",38,-1.8,2)
	ha0nz0 = ROOT.TH1F("ha0n","ha0n",38,-1.8,2)

	hbipz0 = ROOT.TH1F("hbip","hbip",200,-5,5)
	hcipz0 = ROOT.TH1F("hcip","hcip",200,-5,5)
	hqipz0 = ROOT.TH1F("hqip","hqip",200,-5,5)

	hjprobz0 = ROOT.TH1F("hjprob","hjprob",50,0,5)
	hjprob2z0 = ROOT.TH1F("hjprob2","hjprob2",195,5,200)

	# hb/hc/hq/ha0
	ntbb.Project("hb", "log10(abs(sz0))","abs(sz0sig)>5")
	ntcc.Project("hc", "log10(abs(sz0))","abs(sz0sig)>5")
	ntqq.Project("hq", "log10(abs(sz0))","abs(sz0sig)>5")

	ha0z0.Add(hbz0)
	ha0z0.Add(hcz0)
	ha0z0.Add(hqz0)

	# normalize
	hbz0.Divide(ha0z0)
	hcz0.Divide(ha0z0)
	hqz0.Divide(ha0z0)

	print "hb/hc/hq written." 

	# hbp/hcp/hqp/ha0p
	ntbb.Project("hbp", "log10(sz0)","abs(sz0sig)>5&&sz0>0")
	ntcc.Project("hcp", "log10(sz0)","abs(sz0sig)>5&&sz0>0")
	ntqq.Project("hqp", "log10(sz0)","abs(sz0sig)>5&&sz0>0")

	ha0pz0.Add(hbpz0)
	ha0pz0.Add(hcpz0)
	ha0pz0.Add(hqpz0)

	# normalize
	hbpz0.Divide(ha0pz0)
	hcpz0.Divide(ha0pz0)
	hqpz0.Divide(ha0pz0)

	print "hbp/hcp/hqp written." 

	# hbn/hcn/hqn/ha0n
	ntbb.Project("hbn", "log10(-sz0)","abs(sz0sig)>5&&sz0<0")
	ntcc.Project("hcn", "log10(-sz0)","abs(sz0sig)>5&&sz0<0")
	ntqq.Project("hqn", "log10(-sz0)","abs(sz0sig)>5&&sz0<0")

	ha0nz0.Add(hbnz0)
	ha0nz0.Add(hcnz0)
	ha0nz0.Add(hqnz0)

	# normalize
	hbnz0.Divide(ha0nz0)
	hcnz0.Divide(ha0nz0)
	hqnz0.Divide(ha0nz0)

	print "hbn/hcn/hqn written." 

	# hbip/hcip/hqip not normalized
	ntbb.Project("hbip", "sz0sig","abs(sz0sig)<5")
	ntcc.Project("hcip", "sz0sig","abs(sz0sig)<5")
	ntqq.Project("hqip", "sz0sig","abs(sz0sig)<5")

	print "hbip/hcip/hqip written." 

	ntqq.Project("hjprob", "abs(sz0sig)","jprobcut>0")
	ntqq.Project("hjprob2", "abs(sz0sig)","jprobcut>0")

	integ = hjprobz0.Integral(0,50) + hjprob2z0.Integral(0,195)
	hjprobz0.Scale(1./integ)
	hjprob2z0.Scale(1./integ)

	print "hjprob/hjprob2 written." 

	fz0.Write()
	fz0.Close()

	print "All finished." 